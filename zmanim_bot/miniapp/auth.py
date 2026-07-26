import asyncio
import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl

from aiohttp import ClientError, ClientSession, ClientTimeout

# initData is minted when the user opens the mini app, so a generous window
# still forces a fresh signature at least daily.
INIT_DATA_MAX_AGE_SECONDS = 24 * 60 * 60

# A Login Widget payload is minted once, at sign-in on the website, and then
# reused as the sync credential — expiring it forces a fresh sign-in, so the
# window is a session length, not a request guard.
LOGIN_WIDGET_MAX_AGE_SECONDS = 90 * 24 * 60 * 60


def validate_init_data(init_data: str, bot_token: str) -> dict | None:
    """Validate a Mini App initData string and return its parsed fields.

    Implements https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app:
    the `hash` field must equal HMAC-SHA256 of the sorted key=value lines,
    keyed with HMAC-SHA256(bot_token, key='WebAppData'). Returns None when the
    signature is wrong or the data is older than INIT_DATA_MAX_AGE_SECONDS.
    The `user` field is JSON-decoded into a dict.
    """
    try:
        fields = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return None

    received_hash = fields.pop('hash', None)
    if not received_hash:
        return None

    check_string = '\n'.join(f'{key}={value}' for key, value in sorted(fields.items()))
    secret_key = hmac.new(b'WebAppData', bot_token.encode(), hashlib.sha256).digest()
    expected_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_hash, received_hash):
        return None

    try:
        auth_date = int(fields.get('auth_date', '0'))
    except ValueError:
        return None
    if auth_date <= 0 or time.time() - auth_date > INIT_DATA_MAX_AGE_SECONDS:
        return None

    if 'user' in fields:
        try:
            fields['user'] = json.loads(fields['user'])
        except ValueError:
            return None
        if not isinstance(fields['user'], dict) or 'id' not in fields['user']:
            return None

    return fields


def validate_login_widget(data: dict, bot_token: str) -> dict | None:
    """Validate a Telegram Login Widget payload and return its fields.

    Implements https://core.telegram.org/widgets/login#checking-authorization:
    like initData, `hash` must equal HMAC-SHA256 of the sorted key=value
    lines, but the key here is the plain SHA256 of the bot token. Returns
    None when the signature is wrong, the payload is malformed, or older
    than LOGIN_WIDGET_MAX_AGE_SECONDS.
    """
    if not isinstance(data, dict):
        return None
    received_hash = data.get('hash')
    if not isinstance(received_hash, str) or not received_hash:
        return None
    fields = {key: value for key, value in data.items() if key != 'hash'}
    if any(not isinstance(value, (str, int)) for value in fields.values()):
        return None

    check_string = '\n'.join(f'{key}={fields[key]}' for key in sorted(fields))
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    expected_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_hash, received_hash):
        return None

    try:
        auth_date = int(fields.get('auth_date', 0))
    except (TypeError, ValueError):
        return None
    if auth_date <= 0 or time.time() - auth_date > LOGIN_WIDGET_MAX_AGE_SECONDS:
        return None

    if not isinstance(fields.get('id'), int):
        return None
    return fields


GOOGLE_TOKENINFO_URL = 'https://oauth2.googleapis.com/tokeninfo'
GOOGLE_ISSUERS = {'accounts.google.com', 'https://accounts.google.com'}


async def verify_google_id_token(credential: str, client_id: str | None) -> dict | None:
    """Validate a Google ID token and return its claims, or None.

    The site signs in with Google purely to identify which sync blob is
    the user's; the token is verified here, once per device, and never seen
    again — afterwards the site holds the derived key (see api.handle_google_key).

    Verification is delegated to Google's tokeninfo endpoint rather than done
    locally against its public keys. Local verification is what Google
    recommends at volume, but it needs an RSA/JWT stack this project doesn't
    carry (google-auth pulls in a blocking HTTP transport, awkward inside
    aiohttp). This runs once per device per lifetime, so the round trip is
    cheap; swap in local verification here if that ever stops being true.

    The endpoint checks the signature and expiry; `aud` and `iss` are ours to
    check, and an unverified email is refused so a token minted for another
    app or a half-made account can't claim a key.
    """
    if not client_id or not isinstance(credential, str) or not credential:
        return None

    # A short timeout: this is an interactive sign-in, and every call opens its
    # own session, so aiohttp's ~5-minute default would let a Google stall or a
    # burst of junk credentials pin many tasks and outbound connections.
    timeout = ClientTimeout(total=5, connect=3)
    try:
        async with ClientSession(timeout=timeout) as session:
            async with session.get(GOOGLE_TOKENINFO_URL, params={'id_token': credential}) as response:
                if response.status != 200:
                    return None
                claims = await response.json()
    except (ClientError, ValueError, asyncio.TimeoutError):
        return None

    if not isinstance(claims, dict):
        return None
    if claims.get('aud') != client_id:
        return None
    if claims.get('iss') not in GOOGLE_ISSUERS:
        return None
    if str(claims.get('email_verified', 'false')).lower() != 'true':
        return None
    try:
        if int(claims.get('exp', 0)) <= time.time():
            return None
    except (TypeError, ValueError):
        return None
    if not claims.get('sub'):
        return None
    return claims
