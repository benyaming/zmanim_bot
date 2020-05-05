from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from ...misc import dp
from ...handlers.redirects import redirect_to_main_menu
from ...texts import buttons, messages
from ... import keyboards
from ... import api
from ... import zmanim_api
from ...states import ZmanimGregorianDateState


@dp.message_handler(text=buttons.mm_zmanim)
async def handle_zmanim(msg: Message):
    location = await api.get_or_set_location()
    zmanim_settings = await api.get_or_set_zmanim()
    resp = await zmanim_api.get_zmanim(location, zmanim_settings)
    await msg.reply(f'<code>{resp.json(exclude_none=True)}</code>')


@dp.message_handler(text=buttons.mm_shabat)
async def handle_shabbat(msg: Message):
    location = await api.get_or_set_location()
    cl = await api.get_or_set_cl()
    havdala = await api.get_or_set_havdala()
    resp = await zmanim_api.get_shabbat(location, cl, havdala)
    await msg.reply(f'<code>{resp.json(exclude_none=True)}</code>')


@dp.message_handler(text=buttons.mm_daf_yomi)
async def handle_daf_yomi(msg: Message):
    resp = await zmanim_api.get_daf_yomi()
    await msg.reply(f'<code>{resp.json(exclude_none=True)}</code>')


@dp.message_handler(text=buttons.mm_rh)
async def handle_rosh_chodesh(msg: Message):
    resp = await zmanim_api.get_rosh_chodesh()
    await msg.reply(f'<code>{resp.json(exclude_none=True)}</code>')


@dp.message_handler(text=buttons.mm_zmanim_by_date)
async def handle_zmanim_by_date(msg: Message):
    await ZmanimGregorianDateState().waiting_for_gregorian_date.set()
    kb = keyboards.get_cancel_keyboard()
    await msg.reply(messages.greg_date_request, reply_markup=kb)

