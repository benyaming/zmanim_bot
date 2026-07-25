import functools
import inspect

from aiogram.types import ChatActions
from pymongo import IndexModel

from zmanim_bot.misc import collection, db_engine
from zmanim_bot.repository.bot_repository import get_or_set_processor_type
from zmanim_bot.repository.models import WebSync

# Reap settings blobs untouched for this long (see ensure_mongo_index).
WEB_SYNC_TTL_SECONDS = 730 * 24 * 60 * 60


def chat_action(action: str = None):
    def decorator(func):

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            chat_actions = {
                'image': ChatActions.upload_photo,
                'text': ChatActions.typing
            }
            processor_type = action or await get_or_set_processor_type()
            action_func = chat_actions.get(action or processor_type, ChatActions.typing)
            await action_func()

            spec = inspect.getfullargspec(func)
            kwargs = {k: v for k, v in kwargs.items() if k in spec.args}

            return await func(*args, **kwargs)

        return wrapper
    return decorator


async def ensure_mongo_index():
    index = IndexModel('user_id', unique=True)
    await collection.create_indexes([index])
    # The site's key-value sync store lives in its own collection, so its
    # unique index on `key` is declared on the model and created here — without
    # this, lookups scan and two devices racing a first write can duplicate a
    # row (see repository.models.WebSync).
    await db_engine.configure_database([WebSync])
    # TTL: reap blobs no device has touched in a long time. An active device
    # re-writes on every sync, refreshing updated_at, so only truly abandoned
    # rows expire (creation is authenticated, so this is hygiene, not a bound).
    # `account` (a hash of the Google sub) is unique so one account maps to one
    # key, but SPARSE so any pre-account rows (no field) don't collide on null.
    await db_engine.get_collection(WebSync).create_indexes([
        IndexModel('updated_at', expireAfterSeconds=WEB_SYNC_TTL_SECONDS),
        IndexModel('account', unique=True, sparse=True),
    ])
