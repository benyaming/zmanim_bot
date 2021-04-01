from typing import Tuple

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

from zmanim_bot import keyboards
from zmanim_bot import texts
from zmanim_bot.api import storage_api
from zmanim_bot.config import LANGUAGE_SHORTCUTS
from zmanim_bot.helpers import CallbackPrefixes
from zmanim_bot.middlewares.i18n import i18n_
from zmanim_bot.service import zmanim_service
from zmanim_bot.states import FeedbackState


async def get_current_cl() -> Tuple[str, InlineKeyboardMarkup]:
    current_cl = await storage_api.get_or_set_cl()
    kb = keyboards.inline.get_cl_settings_keyboard(current_cl)
    return texts.single.messages.settings_cl, kb


async def set_cl(call_data: str) -> InlineKeyboardMarkup:
    cl = int(call_data.split(CallbackPrefixes.cl)[1])
    await storage_api.get_or_set_cl(cl)

    kb = keyboards.inline.get_cl_settings_keyboard(cl)
    return kb


async def get_current_havdala() -> Tuple[str, InlineKeyboardMarkup]:
    current_havdala = await storage_api.get_or_set_havdala()
    kb = keyboards.inline.get_havdala_settings_keyboard(current_havdala)
    return texts.single.messages.settings_havdala, kb


async def set_havdala(call_data: str) -> InlineKeyboardMarkup:
    havdala = call_data.split(CallbackPrefixes.havdala)[1]
    await storage_api.get_or_set_havdala(havdala)

    kb = keyboards.inline.get_havdala_settings_keyboard(havdala)
    return kb


async def get_current_zmanim() -> Tuple[str, InlineKeyboardMarkup]:
    current_zmanim = await storage_api.get_or_set_zmanim()
    kb = keyboards.inline.get_zmanim_settings_keyboard(current_zmanim)
    return texts.single.messages.settings_havdala, kb


async def set_zmanim(call_data: str) -> InlineKeyboardMarkup:
    zman_name = call_data.split(CallbackPrefixes.zmanim)[1]
    current_zmanim = await storage_api.get_or_set_zmanim()
    current_zmanim[zman_name] = not current_zmanim[zman_name]

    await storage_api.get_or_set_zmanim(current_zmanim)
    kb = keyboards.inline.get_zmanim_settings_keyboard(current_zmanim)
    return kb


async def get_current_omer() -> Tuple[str, InlineKeyboardMarkup]:
    current_omer = await storage_api.get_or_set_omer_flag()
    kb = keyboards.inline.get_omer_kb(current_omer)
    return texts.single.messages.settings_havdala, kb


async def set_omer(call_data) -> InlineKeyboardMarkup:
    omer_flag = not bool(int(call_data.split(CallbackPrefixes.omer)[1]))
    zmanim = omer_flag and await zmanim_service.get_zmanim()
    await storage_api.get_or_set_omer_flag(omer_flag, zmanim)

    kb = keyboards.inline.get_omer_kb(omer_flag)
    return kb


async def set_language(lang: str):
    lang = LANGUAGE_SHORTCUTS[lang]
    await storage_api.get_or_set_lang(lang)
    i18n_.ctx_locale.set(lang)


async def set_location(lat: float, lng: float):
    await storage_api.get_or_set_location((lat, lng))


async def init_report() -> Tuple[str, ReplyKeyboardMarkup]:
    await FeedbackState.waiting_for_feedback_text.set()
    kb = keyboards.menus.get_cancel_keyboard()
    return texts.single.messages.init_report, kb
