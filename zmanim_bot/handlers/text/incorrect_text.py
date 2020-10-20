from aiogram.types import Message

from ...misc import dp
from ...texts.single.messages import incorrect_text
from ...tracking import track


@dp.message_handler()
@track('Incorrect text', attach_message_text=True)
async def handle_incorrect_text(msg: Message):
    await msg.reply(incorrect_text)
