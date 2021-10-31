from aiogram.types import Message
from aiogram_metrics import track

from zmanim_bot.service import festivals_service
from zmanim_bot.utils import chat_action


@chat_action()
@track('Fast')
async def handle_fast(msg: Message):
    await festivals_service.get_generic_fast(msg.text)


@chat_action()
@track('Yom tov')
async def handle_yom_tov(msg: Message):
    await festivals_service.get_generic_yomtov(msg.text)


@chat_action()
@track('Holiday')
async def handle_holiday(msg: Message):
    await festivals_service.get_generic_holiday(msg.text)
