from hashlib import md5
from typing import List

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineQuery, InlineQueryResultLocation, Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified
from aiogram_metrics import track

from zmanim_bot.helpers import CallbackPrefixes, parse_coordinates
from zmanim_bot.integrations.geo_client import get_location_name, find_places_by_query
from zmanim_bot.keyboards import inline
from zmanim_bot.keyboards.menus import get_cancel_keyboard
from zmanim_bot.misc import bot
from zmanim_bot.repository.bot_repository import get_or_create_user
from zmanim_bot.repository.models import User
from zmanim_bot.service import settings_service
from zmanim_bot.states import LocationNameState
from zmanim_bot.texts.single import messages
from zmanim_bot.utils import chat_action


async def get_locations_by_location(lat: float, lng: float, user: User) -> List[InlineQueryResultLocation]:
    location_name = await get_location_name(lat, lng, user.language, no_trim=True)
    result_id = md5(f'{lat}, {lng}'.encode()).hexdigest()
    return [InlineQueryResultLocation(id=result_id, latitude=lat, longitude=lng, title=location_name)]


async def handle_inline_location_query(query: InlineQuery):
    user = await get_or_create_user()

    if len(query.query) < 3:
        if not query.location:
            return  # too short query to search
        results = await get_locations_by_location(query.location.latitude, query.location.longitude, user)
    else:
        results = await find_places_by_query(query.query, user.language)

    await bot.answer_inline_query(query.id, results)


@chat_action('text')
@track('Location menu init')
async def location_settings(msg: Message):
    kb = inline.get_location_management_kb()
    resp = messages.location_menu_init
    await msg.reply(resp, reply_markup=kb)


@track('Location menu back')
async def back_to_location_settings(call: CallbackQuery):
    await call.answer()
    kb = inline.get_location_management_kb()
    resp = messages.location_menu_init
    await bot.edit_message_text(resp, call.from_user.id, call.message.message_id)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)


@track('Location menu -> add new location')
async def add_new_location(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(messages.request_location, call.from_user.id, call.message.message_id)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=inline.LOCATION_SEARCH_KB)


@track('Location menu -> Manage saved locations')
async def manage_saved_locations(call: CallbackQuery):
    await call.answer()
    resp, kb = await settings_service.get_locations_menu()
    await bot.edit_message_text(resp, call.from_user.id, call.message.message_id)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)


async def handle_activate_location(call: CallbackQuery):
    location_name = call.data.split(CallbackPrefixes.location_activate)[1]
    alert, kb = await settings_service.activate_location(location_name)
    await call.answer(alert)

    try:
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)
    except MessageNotModified:
        pass


async def init_location_rename(call: CallbackQuery, state: FSMContext):
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


async def handle_delete_location(call: CallbackQuery):
    location_name = call.data.split(CallbackPrefixes.location_delete)[1]
    alert_text, kb = await settings_service.delete_location(location_name)
    await call.answer(alert_text, show_alert=True)

    if kb:
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)


@track('Location regexp')
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
