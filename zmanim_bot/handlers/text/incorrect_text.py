from aiogram.types import Message

from ...misc import dp
from ...texts.single.messages import incorrect_text


@dp.message_handler()
async def handle_incorrect_text(msg: Message):
    await msg.reply(incorrect_text)
