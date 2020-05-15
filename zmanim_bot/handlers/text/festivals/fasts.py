from aiogram.types import Message

from ....misc import dp
from ....texts.single import buttons
from .... import api
from .... import zmanim_api
from ....processors.image.image_processor import FastPicture


@dp.message_handler(text=buttons.fm_gedaliah)
async def handle_fast_gedaliah(msg: Message):
    location = await api.get_or_set_location()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_fast('fast_gedalia', location, havdala)
    pic = FastPicture().draw_picture(data)
    await msg.reply_photo(pic)


@dp.message_handler(text=buttons.fm_tevet)
async def handle_fast_tevet(msg: Message):
    location = await api.get_or_set_location()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_fast('fast_10_teves', location, havdala)
    pic = FastPicture().draw_picture(data)
    await msg.reply_photo(pic)


@dp.message_handler(text=buttons.fm_esther)
async def handle_fast_esther(msg: Message):
    location = await api.get_or_set_location()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_fast('fast_esther', location, havdala)
    pic = FastPicture().draw_picture(data)
    await msg.reply_photo(pic)


@dp.message_handler(text=buttons.fm_tammuz)
async def handle_fast_tammuz(msg: Message):
    location = await api.get_or_set_location()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_fast('fast_17_tammuz', location, havdala)
    pic = FastPicture().draw_picture(data)
    await msg.reply_photo(pic)


@dp.message_handler(text=buttons.fm_av)
async def handle_fast_av(msg: Message):
    location = await api.get_or_set_location()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_fast('fast_9_av', location, havdala)
    pic = FastPicture().draw_picture(data)
    await msg.reply_photo(pic)
