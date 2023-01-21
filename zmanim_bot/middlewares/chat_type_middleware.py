from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, ChatMemberUpdated

from zmanim_bot.exceptions import UnsupportedChatTypeException

error = 'This bot supports only private chats! Please, remove the bot from the group!'


class ChatTypeMiddleware(BaseMiddleware):

    @staticmethod
    async def on_pre_process_my_chat_member(update: ChatMemberUpdated, *_):
        if update.new_chat_member.status in ('member', 'restricted'):
            await update.bot.send_message(update.chat.id, error)
            raise UnsupportedChatTypeException()

    @staticmethod
    async def on_process_message(msg: Message, *_):
        if msg.chat.type in ('group', 'supergroup') and not msg.left_chat_member:
            await msg.reply(error)
            raise UnsupportedChatTypeException()
