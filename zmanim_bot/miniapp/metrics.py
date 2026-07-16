import json
from datetime import datetime as dt

from aiogram_metrics.hub import Hub
from aiogram_metrics.sql import save_event

from zmanim_bot.misc import logger
from zmanim_bot.repository.models import User

# Custom message_type marking rows that came from the mini app, not a chat.
MESSAGE_TYPE = 'miniapp'


async def track_miniapp_event(event: str, user: User, **details) -> None:
    """Record a mini-app event in the same stats table the bot handlers use.

    aiogram_metrics' track/manual_track need a current aiogram Update, which
    API requests don't have — so the row is written through its storage layer
    directly. Best-effort: stats must never break an API response.
    """
    if not Hub.is_activated:
        return
    try:
        await save_event((
            event,
            dt.now().isoformat(),
            user.user_id,
            None,  # no message behind an API call
            MESSAGE_TYPE,
            json.dumps(details, ensure_ascii=False) if details else None,
            user.language,
        ))
    except Exception as e:
        logger.warning('miniapp: failed to track %r: %s', event, e)
