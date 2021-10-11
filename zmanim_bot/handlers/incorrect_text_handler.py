from aiogram.types import Message
from aiogram_metrics import track

from zmanim_bot.texts.single.messages import incorrect_text
from zmanim_bot.utils import chat_action


@chat_action('text')
@track('Incorrect text')
async def handle_incorrect_text(msg: Message):
    await msg.reply(incorrect_text)

