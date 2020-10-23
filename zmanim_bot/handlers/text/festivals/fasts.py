from aiogram.types import Message

from ....misc import dp
from ....texts.single import buttons
from .... import api
from .... import zmanim_api
from ....processors.image.image_processor import FastImage
from ....tracking import track


@dp.message_handler(text=buttons.fm_gedaliah)
@track('Fast Gedaliah')
async def handle_fast_gedaliah(msg: Message):
    location = await api.get_or_set_location()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_fast('fast_gedalia', location, havdala)
    pic, kb = FastImage(data).get_image()
    await msg.reply_photo(pic, reply_markup=kb)


@dp.message_handler(text=buttons.fm_tevet)
@track('Fast 10th Tevet')
async def handle_fast_tevet(msg: Message):
    location = await api.get_or_set_location()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_fast('fast_10_teves', location, havdala)
    pic, kb = FastImage(data).get_image()
    await msg.reply_photo(pic, reply_markup=kb)


@dp.message_handler(text=buttons.fm_esther)
@track('Fast Esther')
async def handle_fast_esther(msg: Message):
    location = await api.get_or_set_location()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_fast('fast_esther', location, havdala)
    pic, kb = FastImage(data).get_image()
    await msg.reply_photo(pic, reply_markup=kb)


@dp.message_handler(text=buttons.fm_tammuz)
@track('Fast 17th Tammuz')
async def handle_fast_tammuz(msg: Message):
    location = await api.get_or_set_location()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_fast('fast_17_tammuz', location, havdala)
    pic, kb = FastImage(data).get_image()
    await msg.reply_photo(pic, reply_markup=kb)


@dp.message_handler(text=buttons.fm_av)
@track('Fast 9th Av')
async def handle_fast_av(msg: Message):
    location = await api.get_or_set_location()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_fast('fast_9_av', location, havdala)
    pic, kb = FastImage(data).get_image()
    await msg.reply_photo(pic, reply_markup=kb)
