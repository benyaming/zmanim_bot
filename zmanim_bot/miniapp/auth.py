import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl

# initData is minted when the user opens the mini app, so a generous window
# still forces a fresh signature at least daily.
INIT_DATA_MAX_AGE_SECONDS = 24 * 60 * 60


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
