from typing import Optional

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from zmanim_bot.helpers import CallbackPrefixes
from zmanim_bot.integrations import zmanim_api_client
from zmanim_bot.integrations.zmanim_models import Zmanim
from zmanim_bot.keyboards import inline
from zmanim_bot.misc import bot
from zmanim_bot.repository import bot_repository
from zmanim_bot.states import ZmanimGregorianDateState


async def get_zmanim(must_have_8_5: bool = False) -> Zmanim:
    user = await bot_repository.get_or_create_user()
    user_zmanim_settings = user.zmanim_settings

    if must_have_8_5:
        user_zmanim_settings.tzeis_8_5_degrees = True

    data = await zmanim_api_client.get_zmanim(
        user.location.coordinates,
        user_zmanim_settings.dict()
    )
    return data


async def send_zmanim(*, state: FSMContext, date: str = None, call: CallbackQuery = None):
    if call:
        date = call.data.split(CallbackPrefixes.zmanim_by_date)[1]
    user = await bot_repository.get_or_create_user()

    state_data = await state.get_data()
    if state_data.get('current_location'):
        location = user.get_location_by_coords(*state_data['current_location'])
    else:
        location = user.location

    data = await zmanim_api_client.get_zmanim(
        location.coordinates,
        user.zmanim_settings.dict(),
        date_=date
    )
    kb = inline.get_location_variants_menu(
        user.location_list,
        location,
        CallbackPrefixes.update_zmanim,
        date_=date
    )
    await user.get_processor(location=location).send_zmanim(data, kb)
    if call:
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)


async def update_zmanim(lat: float, lng: float, date: Optional[str]):
    user = await bot_repository.get_or_create_user()
    location = user.get_location_by_coords(lat, lng)

    data = await zmanim_api_client.get_zmanim(
        location.coordinates,
        user.zmanim_settings.dict(),
        date_=date
    )
    kb = inline.get_location_variants_menu(
        user.location_list,
        location,
        CallbackPrefixes.update_zmanim,
        date_=date
    )
    await user.get_processor(location).update_zmanim(data, kb)


async def init_zmanim_by_date():
    await ZmanimGregorianDateState().waiting_for_gregorian_date.set()


async def get_shabbat():
    user = await bot_repository.get_or_create_user()
    data = await zmanim_api_client.get_shabbat(
        location=user.location.coordinates,
        cl_offset=user.cl_offset,
        havdala_opinion=user.havdala_opinion
    )
    kb = inline.get_location_variants_menu(user.location_list, user.location, CallbackPrefixes.update_shabbat)
    await user.get_processor().send_shabbat(data, kb)


async def update_shabbat(lat: float, lng: float, state: FSMContext):
    user = await bot_repository.get_or_create_user()
    location = user.get_location_by_coords(lat, lng)
    await state.update_data({'current_location': [lat, lng]})

    data = await zmanim_api_client.get_shabbat(
        location=location.coordinates,
        cl_offset=user.cl_offset,
        havdala_opinion=user.havdala_opinion
    )
    kb = inline.get_location_variants_menu(user.location_list, location, CallbackPrefixes.update_shabbat)
    await user.get_processor(location).update_shabbat(data, kb)


async def get_daf_yomi():
    user = await bot_repository.get_or_create_user()
    data = await zmanim_api_client.get_daf_yomi()
    await user.get_processor().send_daf_yomi(data)


async def get_rosh_chodesh():
    user = await bot_repository.get_or_create_user()
    data = await zmanim_api_client.get_rosh_chodesh()
    await user.get_processor().send_rosh_chodesh(data)
