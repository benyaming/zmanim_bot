from urllib.parse import urlencode

from zmanim_bot.config import config
from zmanim_bot.exceptions import NoLocationException
from zmanim_bot.repository.models import User

# English must be an explicit /en too, even though the site serves it at the
# root: a bare root URL goes through the site's locale detection, and the
# webview's Accept-Language (the phone language) would override the bot
# language. /en redirects to / while pinning the locale cookie.
_LOCALE_PATHS = {'en': '/en', 'he': '/he', 'ru': '/ru'}


def build_miniapp_url(user: User) -> str | None:
    """Mini-app URL personalized with the user's language and active location.

    The location travels as the site's deep-link query (?lat=&lng=&label=) so
    the app opens on the right city instantly, before the /me profile fetch
    lands. Returns None when MINIAPP_URL is not configured — or not HTTPS:
    Telegram rejects plain-http web_app URLs ("only https links are allowed"),
    and that BadRequest would break every main-menu send. A dev http URL still
    serves the API; testing the buttons needs an https tunnel (see
    zmanim_site/docs/telegram-mini-app.md).
    """
    if not config.MINIAPP_URL or not config.MINIAPP_URL.startswith('https://'):
        return None

    url = config.MINIAPP_URL.rstrip('/') + _LOCALE_PATHS.get(user.language or '', '')
    try:
        location = user.location
    except NoLocationException:
        return url

    params = {'lat': location.lat, 'lng': location.lng, 'label': location.name}
    if location.elevation:
        params['elevation'] = location.elevation
    return f'{url}?{urlencode(params)}'
