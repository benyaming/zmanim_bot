from aiogram.types import Message

from zmanim_bot.misc import dp
from zmanim_bot.texts.single.messages import incorrect_text
from zmanim_bot.tracking import track
from zmanim_bot.utils import chat_action


@dp.message_handler()
@chat_action('text')
@track('Incorrect text', attach_message_text=True)
async def handle_incorrect_text(msg: Message):
    await msg.reply(incorrect_text)

