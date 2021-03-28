from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from ..texts.single import buttons
from ..config import LANGUAGE_LIST


def get_lang_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*LANGUAGE_LIST)
    return kb


def get_main_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(buttons.mm_zmanim.value, buttons.mm_shabbat.value, buttons.mm_holidays.value)
    kb.add(buttons.mm_rh.value, buttons.mm_daf_yomi.value, buttons.mm_fasts.value)
    kb.add(buttons.mm_zmanim_by_date.value, buttons.mm_converter.value)
    kb.add(buttons.hm_report.value, buttons.mm_settings.value)
    return kb


# def get_help_menu() -> ReplyKeyboardMarkup:
#     kb = ReplyKeyboardMarkup(resize_keyboard=True)
#     kb.row(buttons.hm_faq.value, buttons.hm_report.value)
#     kb.row(buttons.back.value)
#     return kb


def get_settings_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(buttons.sm_zmanim.value, buttons.sm_candle.value, buttons.sm_havdala.value)
    kb.row(buttons.sm_lang.value, buttons.sm_omer.value, buttons.sm_location.value, buttons.back.value)
    return kb


def get_holidays_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(buttons.hom_rosh_hashana.value, buttons.hom_yom_kippur.value, buttons.hom_succot.value)
    kb.row(buttons.hom_shmini_atzeret.value, buttons.hom_chanukah.value, buttons.hom_purim.value)
    kb.row(buttons.hom_pesach.value, buttons.hom_shavuot.value, buttons.hom_more.value)
    kb.row(buttons.back.value)
    return kb


def get_more_holidays_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(buttons.hom_tu_bishvat.value, buttons.hom_lag_baomer.value, buttons.hom_israel.value)
    kb.row(buttons.mm_holidays.value, buttons.back.value)
    return kb


def get_fast_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(buttons.fm_gedaliah.value, buttons.fm_tevet.value, buttons.fm_esther.value)
    kb.row(buttons.fm_tammuz.value, buttons.fm_av.value)
    kb.row(buttons.back.value)
    return kb


def get_converter_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(buttons.conv_greg_to_jew.value, buttons.conv_jew_to_greg.value)
    kb.row(buttons.back.value)
    return kb


def get_geobutton(with_back: bool = False) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    geobutton = KeyboardButton(text=buttons.geobutton.value, request_location=True)
    kb.row(geobutton) if not with_back else kb.row(buttons.back.value, geobutton)
    return kb


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(buttons.cancel.value)
    return kb


def get_report_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(buttons.cancel.value, buttons.done.value)
    return kb
