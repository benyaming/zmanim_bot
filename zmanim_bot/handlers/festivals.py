from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_metrics import track

from zmanim_bot.helpers import CallbackPrefixes
from zmanim_bot.service import festivals_service
from zmanim_bot.utils import chat_action


@chat_action()
async def handle_fast(msg: Message, state: FSMContext):
    await state.update_data({'current_fast': msg.text})
    await festivals_service.get_generic_fast(msg.text)


async def handle_fast_update(call: CallbackQuery, state: FSMContext):
    coordinates = call.data.split(CallbackPrefixes.update_fast)[1]
    lat, lng = map(float, coordinates.split(','))
    await state.update_data({'current_location': [lat, lng]})

    current_fast_name = (await state.get_data()).get('current_fast')
    if not current_fast_name:
        return await call.answer('Current fast is not set')

    await call.answer()
    await festivals_service.update_generic_fast(current_fast_name, lat, lng)


@chat_action()
async def handle_yom_tov(msg: Message, state: FSMContext):
    await state.update_data({'current_yom_tov': msg.text})
    await festivals_service.get_generic_yomtov(msg.text)


async def handle_yom_tov_update(call: CallbackQuery, state: FSMContext):
    coordinates = call.data.split(CallbackPrefixes.update_yom_tov)[1]
    lat, lng = map(float, coordinates.split(','))
    await state.update_data({'current_location': [lat, lng]})
    
    current_yom_tov_name = (await state.get_data()).get('current_yom_tov')
    if not current_yom_tov_name:
        return await call.answer('Current yom tov is not set')

    await call.answer()

    await festivals_service.update_generic_yom_tov(current_yom_tov_name, lat, lng)


@chat_action()
@track('Holiday')
async def handle_holiday(msg: Message):
    await festivals_service.get_generic_holiday(msg.text)
