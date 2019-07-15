from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, KeyboardButton

import zmanim_bot.texts as txt


def get_main_menu(lang: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(txt.mm_zmanim, txt.mm_shabos, txt.mm_holidays)
    kb.add(txt.mm_rh, txt.mm_daf, txt.mm_fasts)
    kb.add(txt.mm_zmanim_by_date, txt.mm_converter)
    kb.add(txt.mm_help, txt.mm_settings)
    return kb


def get_lang_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add('English', 'Русский')
    return kb


def get_geobutton(lang: str, is_update: bool = False) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text=txt.geobutton, request_location=True)
    kb.row(btn)
    if is_update:
        kb.row(txt.cancel_button)
    return kb


def get_help_menu(lang: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(txt.hm_faq, txt.hm_report)
    kb.row(txt.back_button)
    return kb


def get_settings_menu(lang: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(txt.sm_zmanim, txt.sm_candle, txt.sm_lang)
    kb.row(txt.sm_location, txt.back_button)
    return kb


def get_holidays_menu(lang: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(txt.hom_rosh_hashana, txt.hom_yom_kippur, txt.hom_succos)
    kb.row(txt.hom_shmini_atzeres, txt.hom_chanukah, txt.hom_purim)
    kb.row(txt.hom_pesach, txt.hom_shavuos, txt.hom_more_holidays_button)
    kb.row(txt.back_button)
    return kb


def get_more_holidays_menu(lang: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(txt.hom_tu_bishvat, txt.hom_lag_baomer, txt.hom_israel)
    kb.row(txt.hom_main_holidays_button, txt.back_button)
    return kb


def get_fast_menu(lang: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(txt.fm_fedaliah, txt.fm_tevet, txt.fm_esther)
    kb.row(txt.fm_tammuz, txt.fm_av)
    kb.row(txt.back_button)
    return kb
