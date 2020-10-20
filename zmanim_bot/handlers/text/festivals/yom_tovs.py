from aiogram.types import Message

from ....misc import dp
from ....texts.single import buttons
from .... import api
from .... import zmanim_api
from ....processors.image.image_processor import YomTovImage
from ....tracking import track


@dp.message_handler(text=buttons.hom_rosh_hashana)
@track('Yomtov - Rosh ha-Shana')
async def handle_rosh_hashana(msg: Message):
    location = await api.get_or_set_location()
    cl = await api.get_or_set_cl()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_yomtov('rosh_hashana', location, cl, havdala)
    img = YomTovImage(data).get_image()
    await msg.reply_photo(img)


@dp.message_handler(text=buttons.hom_yom_kippur)
@track('Yomtov - Yom Kippur')
async def handle_yom_kippur(msg: Message):
    location = await api.get_or_set_location()
    cl = await api.get_or_set_cl()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_yomtov('yom_kippur', location, cl, havdala)
    img = YomTovImage(data).get_image()
    await msg.reply_photo(img)


@dp.message_handler(text=buttons.hom_succot)
@track('Yomtov - Succot')
async def handle_succot(msg: Message):
    location = await api.get_or_set_location()
    cl = await api.get_or_set_cl()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_yomtov('succot', location, cl, havdala)
    img = YomTovImage(data).get_image()
    await msg.reply_photo(img)


@dp.message_handler(text=buttons.hom_shmini_atzeret)
@track('Yomtov - Shmini Atzeret')
async def handle_shmini_atzeret(msg: Message):
    location = await api.get_or_set_location()
    cl = await api.get_or_set_cl()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_yomtov('shmini_atzeres', location, cl, havdala)
    img = YomTovImage(data).get_image()
    await msg.reply_photo(img)


@dp.message_handler(text=buttons.hom_pesach)
@track('Yomtov - Pesach')
async def handle_pesach(msg: Message):
    location = await api.get_or_set_location()
    cl = await api.get_or_set_cl()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_yomtov('pesach', location, cl, havdala)
    img = YomTovImage(data).get_image()
    await msg.reply_photo(img)


@dp.message_handler(text=buttons.hom_shavuot)
@track('Yomtov - Shavuot')
async def handle_shavuot(msg: Message):
    location = await api.get_or_set_location()
    cl = await api.get_or_set_cl()
    havdala = await api.get_or_set_havdala()

    data = await zmanim_api.get_generic_yomtov('shavuot', location, cl, havdala)
    img = YomTovImage(data).get_image()
    await msg.reply_photo(img)
