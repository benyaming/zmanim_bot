from aiogram.types import Message

from ....misc import dp
from ....texts.single import buttons
from .... import zmanim_api
from ....processors.image.image_processor import HolidayImage


@dp.message_handler(text=buttons.hom_chanukah)
async def handle_chanukah(msg: Message):
    data = await zmanim_api.get_generic_holiday('chanukah')
    pic = HolidayImage(data).get_image()
    await msg.reply_photo(pic)


@dp.message_handler(text=buttons.hom_tu_bishvat)
async def handle_tu_bi_shvat(msg: Message):
    data = await zmanim_api.get_generic_holiday('tu_bi_shvat')
    pic = HolidayImage(data).get_image()
    await msg.reply_photo(pic)


@dp.message_handler(text=buttons.hom_purim)
async def handle_purim(msg: Message):
    data = await zmanim_api.get_generic_holiday('purim')
    pic = HolidayImage(data).get_image()
    await msg.reply_photo(pic)


@dp.message_handler(text=buttons.hom_israel)
async def handle_israel_holidays(msg: Message):
    data = await zmanim_api.get_generic_holiday('israel_holidays')
    pic = HolidayImage(data).get_image()
    await msg.reply_photo(pic)


@dp.message_handler(text=buttons.hom_lag_baomer)
async def handle_lag_baomer(msg: Message):
    data = await zmanim_api.get_generic_holiday('lag_baomer')
    pic = HolidayImage(data).get_image()
    await msg.reply_photo(pic)
