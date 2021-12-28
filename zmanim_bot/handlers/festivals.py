from aiogram.types import Message, CallbackQuery
from aiogram_metrics import track

from zmanim_bot.helpers import CallbackPrefixes
from zmanim_bot.service import festivals_service
from zmanim_bot.utils import chat_action


@chat_action()
@track('Fast')
async def handle_fast(msg: Message):
    await festivals_service.get_generic_fast(msg.text)


@track('Fast geo-variant')
async def handle_fast_update(call: CallbackQuery):
    await call.answer()
    coordinates = call.data.split(CallbackPrefixes.update_fast)[1]
    lat, lng = map(float, coordinates.split(','))

    # todo                                      this is error, need to use custom callback data (or states?)
    await festivals_service.update_generic_fast(call.message.text, lat, lng)


@chat_action()
@track('Yom tov')
async def handle_yom_tov(msg: Message):
    await festivals_service.get_generic_yomtov(msg.text)


@chat_action()
@track('Holiday')
async def handle_holiday(msg: Message):
    await festivals_service.get_generic_holiday(msg.text)
