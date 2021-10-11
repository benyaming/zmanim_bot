from aiogram.types import Message
from aiogram_metrics import track

from zmanim_bot.service import festivals_service
from zmanim_bot.utils import chat_action


@chat_action()
@track('Fast')
async def handle_fast(msg: Message):
    resp, kb = await festivals_service.get_generic_fast(msg.text)
    await msg.reply_photo(resp, reply_markup=kb)


@chat_action()
@track('Yom tov')
async def handle_yom_tov(msg: Message):
    resp, kb = await festivals_service.get_generic_yomtov(msg.text)
    await msg.reply_photo(resp, reply_markup=kb)


@chat_action()
@track('Holiday')
async def handle_holiday(msg: Message):
    resp = await festivals_service.get_generic_holiday(msg.text)
    await msg.reply_photo(resp)
