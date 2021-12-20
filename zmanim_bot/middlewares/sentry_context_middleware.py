import sentry_sdk
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update


class SentryContextMiddleware(BaseMiddleware):

    @staticmethod
    async def on_pre_process_update(update: Update, _):
        if (not update.message) and (not update.callback_query):
            return

        sentry_sdk.set_user({
            'id': (update.message or update.callback_query).from_user.id,
            'update': update.to_python()
        })
