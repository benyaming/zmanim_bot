from typing import Optional, Tuple

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

from zmanim_bot import keyboards, texts
from zmanim_bot.config import config
from zmanim_bot.exceptions import ActiveLocationException
from zmanim_bot.helpers import CallbackPrefixes
from zmanim_bot.middlewares.i18n import i18n_
from zmanim_bot.repository import bot_repository
from zmanim_bot.service import zmanim_service
from zmanim_bot.states import FeedbackState
from zmanim_bot.texts.single import messages


async def get_current_cl() -> Tuple[str, InlineKeyboardMarkup]:
    current_cl = await bot_repository.get_or_set_cl()
    kb = keyboards.inline.get_cl_settings_keyboard(current_cl)
    return texts.single.messages.settings_cl, kb


async def set_cl(call_data: str) -> InlineKeyboardMarkup:
    cl = int(call_data.split(CallbackPrefixes.cl)[1])
    await bot_repository.get_or_set_cl(cl)

    kb = keyboards.inline.get_cl_settings_keyboard(cl)
    return kb


async def get_current_havdala() -> Tuple[str, InlineKeyboardMarkup]:
    current_havdala = await bot_repository.get_or_set_havdala()
    kb = keyboards.inline.get_havdala_settings_keyboard(current_havdala)
    return texts.single.messages.settings_havdala, kb


async def set_havdala(call_data: str) -> InlineKeyboardMarkup:
    havdala = call_data.split(CallbackPrefixes.havdala)[1]
    await bot_repository.get_or_set_havdala(havdala)

    kb = keyboards.inline.get_havdala_settings_keyboard(havdala)
    return kb


async def get_current_zmanim() -> Tuple[str, InlineKeyboardMarkup]:
    current_zmanim = await bot_repository.get_or_set_zmanim()
    kb = keyboards.inline.get_zmanim_settings_keyboard(current_zmanim)
    return texts.single.messages.settings_zmanim, kb


async def set_zmanim(call_data: str) -> InlineKeyboardMarkup:
    zman_name = call_data.split(CallbackPrefixes.zmanim)[1]
    current_zmanim = await bot_repository.get_or_set_zmanim()
    current_zmanim[zman_name] = not current_zmanim[zman_name]

    await bot_repository.get_or_set_zmanim(current_zmanim)
    kb = keyboards.inline.get_zmanim_settings_keyboard(current_zmanim)
    return kb


async def get_current_omer() -> Tuple[str, InlineKeyboardMarkup]:
    current_omer = await bot_repository.get_or_set_omer_flag()
    kb = keyboards.inline.get_omer_kb(current_omer)
    return texts.single.messages.settings_omer, kb


async def set_omer(call_data: str) -> InlineKeyboardMarkup:
    omer_flag = not bool(int(call_data.split(CallbackPrefixes.omer)[1]))
    zmanim = omer_flag and await zmanim_service.get_zmanim(must_have_8_5=True)
    await bot_repository.get_or_set_omer_flag(omer_flag, zmanim)

    kb = keyboards.inline.get_omer_kb(omer_flag)
    return kb


async def get_current_format() -> Tuple[str, InlineKeyboardMarkup]:
    current_format = await bot_repository.get_or_set_processor_type()
    kb = keyboards.inline.get_format_options_kb(current_format)
    return texts.single.messages.settings_format, kb


async def set_format(call_data: str) -> InlineKeyboardMarkup:
    current_format = call_data.split(CallbackPrefixes.format)[1]
    await bot_repository.get_or_set_processor_type(current_format)

    kb = keyboards.inline.get_format_options_kb(current_format)
    return kb


async def set_language(lang: str):
    lang = config.LANGUAGE_SHORTCUTS[lang]
    await bot_repository.get_or_set_lang(lang)
    i18n_.ctx_locale.set(lang)


async def get_locations_menu() -> Tuple[str, InlineKeyboardMarkup]:
    user = await bot_repository.get_or_create_user()
    kb = keyboards.inline.get_location_options_menu(user.location_list)

    return messages.settings_location, kb


async def save_location(lat: float, lng: float) -> Tuple[str, ReplyKeyboardMarkup, str]:
    location = await bot_repository.get_or_set_location((lat, lng))
    kb = keyboards.menus.get_done_keyboard()
    resp = messages.custom_location_name_request.value.format(location.name)
    return resp, kb, location.name


async def activate_location(location_name: str) -> Tuple[str, InlineKeyboardMarkup]:
    location_list = await bot_repository.activate_location(location_name)
    resp = messages.location_activated.value.format(location_name)
    kb = keyboards.inline.get_location_options_menu(location_list)
    return resp, kb


async def delete_location(location_name: str) -> Tuple[str, Optional[InlineKeyboardMarkup]]:
    try:
        location_list = await bot_repository.delete_location(location_name)
        kb = keyboards.inline.get_location_options_menu(location_list)
        msg = messages.location_deleted
    except ActiveLocationException:
        kb = None
        msg = messages.unable_to_delete_active_location

    return msg, kb


async def update_location_name(new_name: str, old_name: Optional[str]) -> InlineKeyboardMarkup:
    if not old_name:
        raise ValueError('There is no old location name!')

    location_list = await bot_repository.set_location_name(new_name=new_name, old_name=old_name)
    kb = keyboards.inline.get_location_options_menu(location_list)
    return kb


async def init_report() -> Tuple[str, ReplyKeyboardMarkup]:
    await FeedbackState.waiting_for_feedback_text.set()
    kb = keyboards.menus.get_cancel_keyboard()
    return texts.single.messages.init_report, kb
