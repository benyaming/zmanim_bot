from aiogram.types import Message

from ...misc import dp
from ...texts import buttons, messages
from ... import keyboards
from ... import api
from ... import zmanim_api
from ...states import ZmanimGregorianDateState
from ...processors.image import image_processor as ip


@dp.message_handler(text=buttons.mm_zmanim)
async def handle_zmanim(msg: Message):
    location = await api.get_or_set_location()
    zmanim_settings = await api.get_or_set_zmanim()
    resp = await zmanim_api.get_zmanim(location, zmanim_settings)
    await msg.reply(f'<code>{resp.json(exclude_none=True, indent=2, by_alias=True)}</code>')


@dp.message_handler(text=buttons.mm_shabbat)
async def handle_shabbat(msg: Message):
    location = await api.get_or_set_location()
    cl = await api.get_or_set_cl()
    havdala = await api.get_or_set_havdala()
    resp = await zmanim_api.get_shabbat(location, cl, havdala)
    await msg.reply(f'<code>{resp.json(exclude_none=True, indent=2, by_alias=True)}</code>')


@dp.message_handler(text=buttons.mm_daf_yomi)
async def handle_daf_yomi(msg: Message):
    data = await zmanim_api.get_daf_yomi()
    pic = ip.DafYomPicture().get_image(data)
    await msg.reply_photo(pic)


@dp.message_handler(text=buttons.mm_rh)
async def handle_rosh_chodesh(msg: Message):
    resp = await zmanim_api.get_rosh_chodesh()
    await msg.reply(f'<code>{resp.json(exclude_none=True, indent=2, by_alias=True)}</code>')


@dp.message_handler(text=buttons.mm_zmanim_by_date)
async def handle_zmanim_by_date(msg: Message):
    await ZmanimGregorianDateState().waiting_for_gregorian_date.set()
    kb = keyboards.get_cancel_keyboard()
    await msg.reply(messages.greg_date_request, reply_markup=kb)


# @dp.message_handler(text=[*buttons.HOLIDAYS, *buttons.FASTS])
# async def holidays_and_fasts_handler(msg: Message):
#
#     location = await api.get_or_set_location() if msg.text else None
#     cl = await api.get_or_set_cl()
#     havdala = await api.get_or_set_havdala()
#
#     resp = await zmanim_api.get_holiday(
#         name=get_holiday_shrtcut(msg.text),
#         cl_offset=cl,
#         havdala_opinion=havdala,
#         location=location
#     )
#     await msg.reply(f'<code>{resp.json(exclude_none=True)}</code>')

