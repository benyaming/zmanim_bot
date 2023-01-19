from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from zmanim_bot.exceptions import AccessDeniedException


class BlackListMiddleware(BaseMiddleware):

    async def trigger(self, action, args):
        if action not in ('pre_process_message', 'pre_process_callback_query'):
            return

        match args[0]:
            case types.Message() as msg:
                chat_type = msg.chat.type
            case types.CallbackQuery() as call:
                chat_type = call.message.chat
            case _:
                return

        if chat_type != 'private':
            return

        from zmanim_bot.repository.bot_repository import get_or_create_user

        user = await get_or_create_user()
        if user.meta.is_banned_by_admin:
            raise AccessDeniedException()

