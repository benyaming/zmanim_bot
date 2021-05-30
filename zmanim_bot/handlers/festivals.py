from aiogram.types import Message
from aiogram_metrics import track

from zmanim_bot.misc import dp
from zmanim_bot.service import festivals_service
from zmanim_bot.texts.single import buttons
from zmanim_bot.utils import chat_action


@dp.message_handler(text=buttons.FASTS)
@chat_action()
@track('Fast')
async def handle_fast(msg: Message):
    resp, kb = await festivals_service.get_generic_fast(msg.text)
    await msg.reply_photo(resp, reply_markup=kb)


@dp.message_handler(text=buttons.YOMTOVS)
@chat_action()
@track('Yom tov')
async def handle_fast(msg: Message):
    resp, kb = await festivals_service.get_generic_yomtov(msg.text)
    await msg.reply_photo(resp, reply_markup=kb)


@dp.message_handler(text=buttons.HOLIDAYS)
@chat_action()
@track('Holiday')
async def handle_fast(msg: Message):
    resp = await festivals_service.get_generic_holiday(msg.text)
    await msg.reply_photo(resp)
