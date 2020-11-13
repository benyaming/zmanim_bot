import asyncio

from aiogram.types import CallbackQuery

from ...keyboards.inline import (
    get_zmanim_settings_keyboard,
    get_havdala_settings_keyboard,
    get_cl_settings_keyboard
)
from ... import api
from ...misc import dp, bot
from ...helpers import CallbackPrefixes, CALL_ANSWER_OK


@dp.callback_query_handler(text_startswith=CallbackPrefixes.cl)
async def handle_cl_call(call: CallbackQuery):
    cl = int(call.data.split(CallbackPrefixes.cl)[1])
    await call.answer(CALL_ANSWER_OK)
    kb = get_cl_settings_keyboard(cl)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)
    asyncio.create_task(api.get_or_set_cl(cl))


@dp.callback_query_handler(text_startswith=CallbackPrefixes.havdala)
async def handle_havdala_call(call: CallbackQuery):
    havdala = call.data.split(CallbackPrefixes.havdala)[1]
    await call.answer(CALL_ANSWER_OK)
    kb = get_havdala_settings_keyboard(havdala)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)
    asyncio.create_task(api.get_or_set_havdala(havdala))


@dp.callback_query_handler(text_startswith=CallbackPrefixes.zmanim)
async def handle_zmanim_call(call: CallbackQuery):
    await call.answer(CALL_ANSWER_OK)
    zman_name = call.data.split(CallbackPrefixes.zmanim)[1]
    current_zmanim = await api.get_or_set_zmanim()
    current_zmanim[zman_name] = not current_zmanim[zman_name]
    kb = get_zmanim_settings_keyboard(current_zmanim)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)
    asyncio.create_task(api.get_or_set_zmanim(current_zmanim))

