"""HTTP API the mini app calls to read and sync the user's bot settings.

Registered under `{WEBHOOK_PATH}/miniapp` — on the webhook server's app in
prod, on a standalone dev server in polling mode (see main.py). Routes are
added directly (NOT via add_subapp: the pinned aiohttp 3.8.6 resolves sub-app
prefixes through `request.url`, which the pinned yarl rejects when the Host
header carries a port) and the CORS middleware scopes itself by path prefix,
so the webhook route is untouched. Auth is stateless: every request carries
the Mini App initData string, validated against the bot token
(auth.validate_init_data). CORS allows only the MINIAPP_URL origin in prod,
anything in dev.

  POST /me    {init_data}                                    -> profile
  POST /sync  {init_data, location? | cl_offset? | havdala_opinion?} -> profile

The profile is {language, cl_offset, havdala_opinion, location{lat,lng,name,
elevation} | null, locations[...]}. Sync mirrors the bot's own location
semantics: matching coordinates re-activate the saved entry; a new place is
appended while under LOCATION_NUMBER_LIMIT. At the limit a new place is NOT
applied — the bot's saved list is user-curated and never overwritten from the
mini app (the app keeps its local choice; the rest of the sync still applies).
"""

import html
import io
from urllib.parse import urlsplit

from aiogram import types
from aiohttp import web

from zmanim_bot.config import config
from zmanim_bot.exceptions import NoLocationException
from zmanim_bot.middlewares.i18n import i18n_
from zmanim_bot.misc import bot, db_engine, logger
from zmanim_bot.repository._storage import MAX_LOCATION_NAME_SIZE, _get_or_create_user
from zmanim_bot.repository.models import HAVDALA_OPINIONS, Location, User
from zmanim_bot.texts.single import buttons, messages
from zmanim_bot.texts.single import zmanim as zmanim_texts

from .auth import validate_init_data
from .metrics import track_miniapp_event

CL_OFFSET_MIN = 1
CL_OFFSET_MAX = 120

# Generous cap for relayed export files (multi-page PDF renders run a few MB;
# Telegram bots can send up to 50 MB).
MAX_EXPORT_BYTES = 30 * 1024 * 1024


def _origin_allowed(origin: str) -> bool:
    if not config.IS_PROD:
        return True
    if not config.MINIAPP_URL:
        return False
    allowed = urlsplit(config.MINIAPP_URL)
    got = urlsplit(origin)
    return (got.scheme, got.netloc) == (allowed.scheme, allowed.netloc)


def _make_cors_middleware(prefix: str):
    """CORS + preflight handling for the mini-app routes only; everything
    outside `prefix` (i.e. the Telegram webhook) passes through untouched."""

    @web.middleware
    async def cors_middleware(request: web.Request, handler) -> web.StreamResponse:
        if not request.path.startswith(prefix):
            return await handler(request)

        if request.method == 'OPTIONS':
            response: web.StreamResponse = web.Response(status=204)
        else:
            try:
                response = await handler(request)
            except web.HTTPException as exc:
                response = exc

        origin = request.headers.get('Origin')
        if origin and _origin_allowed(origin):
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            response.headers['Access-Control-Max-Age'] = '3600'
            response.headers.setdefault('Vary', 'Origin')
        return response

    return cors_middleware


async def _user_from_init_data(init_data) -> User:
    """Validate an initData string and return the bot user it belongs to."""
    if not isinstance(init_data, str) or not init_data:
        raise web.HTTPUnauthorized(reason='Missing init_data')

    parsed = validate_init_data(init_data, config.BOT_TOKEN)
    if not parsed or 'user' not in parsed:
        raise web.HTTPUnauthorized(reason='Invalid init_data')

    info = parsed['user']
    tg_user = types.User(
        id=info['id'],
        is_bot=info.get('is_bot', False),
        first_name=info.get('first_name'),
        last_name=info.get('last_name'),
        username=info.get('username'),
        language_code=info.get('language_code'),
    )
    return await _get_or_create_user(tg_user)


async def _authorize(request: web.Request) -> tuple[User, dict]:
    """Validate a JSON request's initData and return the bot user + body."""
    try:
        body = await request.json()
    except ValueError:
        raise web.HTTPBadRequest(reason='Invalid JSON body')
    user = await _user_from_init_data(body.get('init_data'))
    return user, body


def _location_payload(location: Location) -> dict:
    return {
        'lat': location.lat,
        'lng': location.lng,
        'name': location.name,
        'elevation': location.elevation or 0,
    }


def _profile_payload(user: User) -> dict:
    try:
        location = _location_payload(user.location)
    except NoLocationException:
        location = None
    return {
        'language': user.language,
        'cl_offset': user.cl_offset,
        'havdala_opinion': user.havdala_opinion,
        'location': location,
        # The whole saved list, so the mini app can offer them like the bot does.
        'locations': [_location_payload(loc) for loc in user.location_list],
    }


def _unique_location_name(name: str, locations: list[Location]) -> str:
    """The bot's location UI addresses entries by name, so names must be unique."""
    existing = {loc.name for loc in locations}
    if name not in existing:
        return name
    for i in range(2, 100):
        suffix = f' ({i})'
        candidate = name[: MAX_LOCATION_NAME_SIZE - len(suffix)] + suffix
        if candidate not in existing:
            return candidate
    return name  # 99 clashes: give up on uniqueness rather than fail the sync


def _apply_location(user: User, data) -> bool:
    """Apply a location change; returns False when it can't be (list full)."""
    if not isinstance(data, dict):
        raise web.HTTPBadRequest(reason='location must be an object')
    try:
        lat = float(data['lat'])
        lng = float(data['lng'])
    except (KeyError, TypeError, ValueError):
        raise web.HTTPBadRequest(reason='location.lat/lng must be numbers')
    if not (-90 <= lat <= 90 and -180 <= lng <= 180):
        raise web.HTTPBadRequest(reason='location.lat/lng out of range')

    existing = next((loc for loc in user.location_list if loc.lat == lat and loc.lng == lng), None)
    if existing is None and len(user.location_list) >= config.LOCATION_NUMBER_LIMIT:
        # The saved list is user-curated and at its limit — never replace or
        # evict entries from the mini app. The app keeps its local choice.
        return False

    name = str(data.get('name') or '').strip() or f'{lat:.3f}, {lng:.3f}'
    if len(name) > MAX_LOCATION_NAME_SIZE:
        name = f'{name[:MAX_LOCATION_NAME_SIZE]}...'
    try:
        elevation = max(0, int(data.get('elevation') or 0))
    except (TypeError, ValueError):
        elevation = 0

    for loc in user.location_list:
        loc.is_active = False
    if existing:
        existing.is_active = True
    else:
        name = _unique_location_name(name, user.location_list)
        user.location_list.append(Location(lat=lat, lng=lng, name=name, is_active=True, elevation=elevation))
    return True


def _format_change(label, old, new) -> str:
    """One italic '• Label: old → new' line; without the arrow part when there
    was no previous value (e.g. a first location)."""
    new_text = html.escape(str(new))
    if old is None:
        return f'<i>• {label}: {new_text}</i>'
    return f'<i>• {label}: {html.escape(str(old))} → {new_text}</i>'


async def _notify_settings_changed(user: User, changes: list) -> None:
    """Silent confirmation in the bot chat, so a mini-app change never goes
    unnoticed. Best-effort: a failed send (blocked bot, deleted chat) must not
    fail the sync itself."""
    lines = [f'<i>{messages.miniapp_settings_changed}</i>']
    lines += [_format_change(label, old, new) for label, old, new in changes]
    try:
        await bot.send_message(user.user_id, '\n'.join(lines), disable_notification=True)
    except Exception as e:
        logger.warning('miniapp: could not notify %s about a settings change: %s', user.user_id, e)


async def handle_me(request: web.Request) -> web.Response:
    user, _ = await _authorize(request)
    # /me fires once per launch — the "calendar opened" stats event.
    await track_miniapp_event('Mini app opened', user)
    return web.json_response(_profile_payload(user))


async def handle_sync(request: web.Request) -> web.Response:
    user, body = await _authorize(request)
    # The API runs outside aiogram's handler context, so the lazy gettext
    # strings (labels and values below) need the locale set for this task.
    i18n_.ctx_locale.set(user.language or 'en')

    # (label, old, new) display values for the confirmation message; `old` is
    # None when there was nothing before. No-op writes are saved but not
    # announced (nothing visibly changed).
    changes: list = []
    changed = False

    if body.get('location') is not None:
        try:
            old_location = user.location.name
        except NoLocationException:
            old_location = None
        if _apply_location(user, body['location']):
            changed = True
            if user.location.name != old_location:
                changes.append((buttons.sm_location, old_location, user.location.name))

    cl_offset = body.get('cl_offset')
    if cl_offset is not None:
        if not isinstance(cl_offset, int) or not CL_OFFSET_MIN <= cl_offset <= CL_OFFSET_MAX:
            raise web.HTTPBadRequest(reason='cl_offset out of range')
        if cl_offset != user.cl_offset:
            changes.append((
                buttons.sm_candle,
                f'{user.cl_offset} {messages.minutes_short}',
                f'{cl_offset} {messages.minutes_short}',
            ))
        user.cl_offset = cl_offset
        changed = True

    havdala = body.get('havdala_opinion')
    if havdala is not None:
        if havdala not in HAVDALA_OPINIONS:
            raise web.HTTPBadRequest(reason='Unknown havdala_opinion')
        if havdala != user.havdala_opinion:
            changes.append((
                buttons.sm_havdala,
                # A stored opinion should always have a display name; fall back
                # to the raw key rather than crash the sync if it ever doesn't.
                getattr(zmanim_texts, user.havdala_opinion, user.havdala_opinion),
                getattr(zmanim_texts, havdala),
            ))
        user.havdala_opinion = havdala
        changed = True

    if changed:
        await db_engine.save(user)
        fields = [key for key in ('location', 'cl_offset', 'havdala_opinion') if body.get(key) is not None]
        await track_miniapp_event('Mini app settings sync', user, fields=fields)
    if changes:
        await _notify_settings_changed(user, changes)
    return web.json_response(_profile_payload(user))


async def handle_export(request: web.Request) -> web.Response:
    """Relay an export file to the user's chat — the Telegram webview can't
    download files, so the mini app posts them here (multipart: init_data
    field + file part) and the bot delivers as a document."""
    if not (request.content_type or '').startswith('multipart/'):
        raise web.HTTPBadRequest(reason='multipart/form-data expected')

    init_data = None
    filename = None
    content = None
    reader = await request.multipart()
    async for part in reader:
        if part.name == 'init_data':
            init_data = (await part.read(decode=True)).decode('utf-8', 'replace')
        elif part.name == 'file':
            filename = (part.filename or 'export').rsplit('/', 1)[-1][:120]
            # Stream with a size cap — client_max_size doesn't govern multipart.
            chunks = []
            size = 0
            while True:
                chunk = await part.read_chunk(64 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                if size > MAX_EXPORT_BYTES:
                    raise web.HTTPRequestEntityTooLarge(max_size=MAX_EXPORT_BYTES, actual_size=size)
                chunks.append(chunk)
            content = b''.join(chunks)

    user = await _user_from_init_data(init_data)
    if not content or not filename:
        raise web.HTTPBadRequest(reason='Missing file')

    try:
        await bot.send_document(user.user_id, types.InputFile(io.BytesIO(content), filename=filename))
    except Exception as e:
        logger.warning('miniapp: could not deliver export %r to %s: %s', filename, user.user_id, e)
        raise web.HTTPBadGateway(reason='Could not deliver the file')
    await track_miniapp_event('Mini app export', user, filename=filename)
    return web.json_response({'ok': True})


def register_miniapp_api(app: web.Application, prefix: str) -> None:
    """Add the mini-app API (routes + scoped CORS) to an existing app."""
    app.middlewares.append(_make_cors_middleware(prefix))
    app.router.add_post(f'{prefix}/me', handle_me)
    app.router.add_post(f'{prefix}/sync', handle_sync)
    app.router.add_post(f'{prefix}/export', handle_export)
