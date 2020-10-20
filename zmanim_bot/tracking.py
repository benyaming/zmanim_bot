import inspect

import posthog
from aiogram.types import User, Message

from .config import POSTHOG_API_KEY, IS_PROD


posthog.api_key = POSTHOG_API_KEY
posthog.disabled = not IS_PROD


def track(action: str, params: dict = None, attach_message_text: bool = False):
    params = params if params else {}

    def decorator(func):

        async def wrapper(*args, **kwargs):
            spec = inspect.getfullargspec(func)
            kwargs = {k: v for k, v in kwargs.items() if k in spec.args}

            user = User.get_current()
            msg = Message.get_current()
            attach_message_text and params.update({'text': msg.text})

            posthog.capture(user.id, action, params, message_id=msg.message_id)

            return await func(*args, **kwargs)

        return wrapper
    return decorator
