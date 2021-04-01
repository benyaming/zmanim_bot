from aiogram.types import Message

from zmanim_bot.misc import dp
from zmanim_bot.texts.single import buttons
from zmanim_bot.api import zmanim_api
from zmanim_bot.processors.image.image_processor import HolidayImage, IsraelHolidaysImage
from zmanim_bot.tracking import track
from zmanim_bot.utils import chat_action


@dp.message_handler(text=buttons.hom_chanukah)
@chat_action()
@track('Holiday - Channukah')
async def handle_chanukah(msg: Message):
    data = await zmanim_api.get_generic_holiday('chanukah')
    pic = HolidayImage(data).get_image()
    await msg.reply_photo(pic)


@dp.message_handler(text=buttons.hom_tu_bishvat)
@chat_action()
@track('Holiday - Tu bi-Shvat')
async def handle_tu_bi_shvat(msg: Message):
    data = await zmanim_api.get_generic_holiday('tu_bi_shvat')
    pic = HolidayImage(data).get_image()
    await msg.reply_photo(pic)


@dp.message_handler(text=buttons.hom_purim)
@chat_action()
@track('Holiday - Purim')
async def handle_purim(msg: Message):
    data = await zmanim_api.get_generic_holiday('purim')
    pic = HolidayImage(data).get_image()
    await msg.reply_photo(pic)


@dp.message_handler(text=buttons.hom_israel)
@chat_action()
@track('Holiday - Israel holidays')
async def handle_israel_holidays(msg: Message):
    data = await zmanim_api.get_israel_holidays()
    pic = IsraelHolidaysImage(data).get_image()
    await msg.reply_photo(pic)


@dp.message_handler(text=buttons.hom_lag_baomer)
@chat_action()
@track('Holiday - Lag ba-Omer')
async def handle_lag_baomer(msg: Message):
    data = await zmanim_api.get_generic_holiday('lag_baomer')
    pic = HolidayImage(data).get_image()
    await msg.reply_photo(pic)
