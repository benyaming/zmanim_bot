import inspect

from aiogram.types import ChatActions
from pymongo import IndexModel

from zmanim_bot.misc import collection
from zmanim_bot.repository.bot_repository import get_or_set_processor_type


def chat_action(action: str = None):
    def decorator(func):

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
