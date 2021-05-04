from typing import Tuple, Optional, List

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

from zmanim_bot import keyboards
from zmanim_bot import texts
from zmanim_bot.repository import bot_repository
from zmanim_bot.config import LANGUAGE_SHORTCUTS
from zmanim_bot.exceptions import ActiveLocationException
from zmanim_bot.helpers import CallbackPrefixes
from zmanim_bot.middlewares.i18n import i18n_
from zmanim_bot.service import zmanim_service
from zmanim_bot.states import FeedbackState


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
    return texts.single.messages.settings_havdala, kb


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


async def set_omer(call_data) -> InlineKeyboardMarkup:
    omer_flag = not bool(int(call_data.split(CallbackPrefixes.omer)[1]))
    zmanim = omer_flag and await zmanim_service.get_zmanim()
    await bot_repository.get_or_set_omer_flag(omer_flag, zmanim)

    kb = keyboards.inline.get_omer_kb(omer_flag)
    return kb


async def set_language(lang: str):
    lang = LANGUAGE_SHORTCUTS[lang]
    await bot_repository.get_or_set_lang(lang)
    i18n_.ctx_locale.set(lang)


async def get_locations_menu() -> Tuple[str, InlineKeyboardMarkup]:
    user = await bot_repository.get_or_create_user()
    msg = 'Activate, edit or send new location:'  # todo translate
    kb = keyboards.inline.get_location_options_menu(user.location_list)

    return msg, kb


async def set_location(lat: float, lng: float) -> Tuple[str, ReplyKeyboardMarkup, str]:
    location = await bot_repository.get_or_set_location((lat, lng))
    kb = keyboards.menus.get_done_keyboard()
    resp = f'current name: {location.name}. If yoy want, you can write custom name for the ' \
           f'location or press "Done" button.'  # todo translate
    return resp, kb, location.name


async def activate_location(location_name: str) -> InlineKeyboardMarkup:
    location_list = await bot_repository.activate_location(location_name)
    kb = keyboards.inline.get_location_options_menu(location_list)
    return kb


async def delete_location(location_name: str) -> Tuple[str, Optional[InlineKeyboardMarkup]]:
    try:
        location_list = await bot_repository.delete_location(location_name)
        kb = keyboards.inline.get_location_options_menu(location_list)
        msg = 'Successfully deleted'  # todo translate
    except ActiveLocationException:
        kb = None
        msg = 'Unable to delete active location!'  # todo translate

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


