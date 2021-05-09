from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType, Message

from zmanim_bot.config import LANGUAGE_LIST
from zmanim_bot.handlers.utils.redirects import (redirect_to_main_menu,
                                                 redirect_to_request_language)
from zmanim_bot.helpers import (CALL_ANSWER_OK, LOCATION_PATTERN,
                                CallbackPrefixes, parse_coordinates)
from zmanim_bot.keyboards.menus import get_cancel_keyboard
from zmanim_bot.misc import bot, dp
from zmanim_bot.service import settings_service
from zmanim_bot.states import LocationNameState
from zmanim_bot.texts.single import buttons, messages
from zmanim_bot.tracking import track
from zmanim_bot.utils import chat_action


@dp.message_handler(text=buttons.sm_candle)
@chat_action('text')
@track('Candle lighting selection')
async def settings_menu_cl(msg: Message):
    resp, kb = await settings_service.get_current_cl()
    await msg.reply(resp, reply_markup=kb)


@dp.callback_query_handler(text_startswith=CallbackPrefixes.cl)
async def set_cl(call: CallbackQuery):
    await call.answer(CALL_ANSWER_OK)

    kb = await settings_service.set_cl(call.data)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)


@dp.message_handler(text=buttons.sm_havdala)
@chat_action('text')
@track('Havdala selection')
async def settings_menu_havdala(msg: Message):
    resp, kb = await settings_service.get_current_havdala()
    await msg.reply(resp, reply_markup=kb)


@dp.callback_query_handler(text_startswith=CallbackPrefixes.havdala)
async def set_havdala(call: CallbackQuery):
    await call.answer(CALL_ANSWER_OK)

    kb = await settings_service.set_havdala(call.data)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)


@dp.message_handler(text=buttons.sm_zmanim)
@track('Zmanim selection')
async def settings_menu_zmanim(msg: Message):
    resp, kb = await settings_service.get_current_zmanim()
    await msg.reply(resp, reply_markup=kb)


@dp.callback_query_handler(text_startswith=CallbackPrefixes.zmanim)
async def set_zmanim(call: CallbackQuery):
    await call.answer(CALL_ANSWER_OK)

    kb = await settings_service.set_zmanim(call.data)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)


@dp.message_handler(text=buttons.sm_omer)
@chat_action('text')
@track('Omer Settings')
async def handle_omer_settings(msg: Message):
    resp, kb = await settings_service.get_current_omer()
    await msg.reply(resp, reply_markup=kb)


@dp.callback_query_handler(text_startswith=CallbackPrefixes.omer)
async def set_omer(call: CallbackQuery):
    await call.answer(CALL_ANSWER_OK)

    kb = await settings_service.set_omer(call.data)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)


@dp.message_handler(commands=['language'])
@dp.message_handler(text=buttons.sm_lang)
@chat_action('text')
@track('Language command')
async def handle_language_request(msg: Message):
    await redirect_to_request_language()


@dp.message_handler(text=LANGUAGE_LIST)
@chat_action('text')
@track('Language selected', attach_message_text=True)
async def set_language(msg: Message):
    await settings_service.set_language(msg.text)
    return await redirect_to_main_menu()


@dp.message_handler(commands=['location'])
@dp.message_handler(text=buttons.sm_location)
@chat_action('text')
@track('Location menu')
async def location_request(msg: Message):
    resp, kb = await settings_service.get_locations_menu()
    await msg.reply(resp, reply_markup=kb)


@dp.callback_query_handler(text_startswith=CallbackPrefixes.location_activate)
async def handle_activate_location(call: CallbackQuery):
    location_name = call.data.split(CallbackPrefixes.location_activate)[1]
    alert, kb = await settings_service.activate_location(location_name)
    await call.answer(alert)

    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)


@dp.callback_query_handler(text_startswith=CallbackPrefixes.location_rename)
async def init_location_raname(call: CallbackQuery, state: FSMContext):
    await LocationNameState.waiting_for_location_name_state.set()
    location_name = call.data.split(CallbackPrefixes.location_rename)[1]

    state_data = {
        'location_name': location_name,
        'redirect_target': 'settings',
        'redirect_message': messages.location_renamed.value,
        'origin_message_id': call.message.message_id
    }

    await state.set_data(state_data)
    await call.answer()

    resp = messages.location_new_name_request.value.format(location_name)
    kb = get_cancel_keyboard()
    await bot.send_message(call.from_user.id, resp, reply_markup=kb)


@dp.callback_query_handler(text_startswith=CallbackPrefixes.location_delete)
async def handle_delete_location(call: CallbackQuery):
    location_name = call.data.split(CallbackPrefixes.location_delete)[1]
    alert_text, kb = await settings_service.delete_location(location_name)
    await call.answer(alert_text, show_alert=True)

    if kb:
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)


@dp.message_handler(regexp=LOCATION_PATTERN)
@track('Location regexp')
@dp.message_handler(content_types=[ContentType.LOCATION, ContentType.VENUE])
async def handle_location(msg: Message, state: FSMContext):
    if msg.location:
        lat = msg.location.latitude
        lng = msg.location.longitude
    else:
        lat, lng = parse_coordinates(msg.text)

    resp, kb, location_name = await settings_service.save_location(lat, lng)
    await LocationNameState().waiting_for_location_name_state.set()
    await state.set_data({
        'location_name': location_name,
        'redirect_message': messages.location_saved.value
    })
    await msg.reply(resp, reply_markup=kb)


@dp.message_handler(commands=['report'])
@dp.message_handler(text=buttons.hm_report)
@chat_action('text')
@track('Init report')
async def help_menu_report(msg: Message):
    resp, kb = await settings_service.init_report()
    await msg.reply(resp, reply_markup=kb)
