from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from . import config
from .texts.single import buttons, zmanim
from .helpers import CallbackPrefixes, CL_OFFET_OPTIONS, HAVDALA_OPINION_OPTIONS


def get_lang_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*config.LANGUAGE_LIST)
    return kb


def get_main_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(buttons.mm_zmanim.value, buttons.mm_shabbat.value, buttons.mm_holidays.value)
    kb.add(buttons.mm_rh.value, buttons.mm_daf_yomi.value, buttons.mm_fasts.value)
    kb.add(buttons.mm_zmanim_by_date.value, buttons.mm_converter.value)
    kb.add(buttons.mm_help.value, buttons.mm_settings.value)
    return kb


def get_geobutton(with_back: bool = False) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    geobutton = KeyboardButton(text=buttons.geobutton.value, request_location=True)
    kb.row(geobutton) if not with_back else kb.row(buttons.back.value, geobutton)
    return kb


def get_help_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(buttons.hm_faq.value, buttons.hm_report.value)
    kb.row(buttons.back.value)
    return kb


def get_settings_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(buttons.sm_zmanim.value, buttons.sm_candle.value, buttons.sm_havdala.value)
    kb.row(buttons.sm_lang.value, buttons.sm_location.value, buttons.back.value)
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
    # kb.row()
    kb.row(buttons.back.value)
    return kb


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(buttons.cancel.value)
    return kb


def get_cl_keyboard(current_value: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    row_1 = []
    row_2 = []

    for i, option in enumerate(CL_OFFET_OPTIONS):
        button = InlineKeyboardButton(
            text=f'{option}' if option != current_value else f'✅ {option}',
            callback_data=f'{CallbackPrefixes.cl}{option}'
        )
        row_1.append(button) if i < 3 else row_2.append(button)

    kb.row(*row_1)
    kb.row(*row_2)
    return kb


def get_havdala_keyboard(current_value: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    for option in HAVDALA_OPINION_OPTIONS:
        button = InlineKeyboardButton(
            text=f'{option}' if option != current_value else f'✅ {option}',
            callback_data=f'{CallbackPrefixes.havdala}{option}'
        )
        kb.add(button)
    return kb


def get_zman_button(name: str, status: bool) -> InlineKeyboardButton:
    button = InlineKeyboardButton(
        text=f'{"✅" if status else "❌"} {getattr(zmanim, name)}',
        callback_data=f'{CallbackPrefixes.zmanim}{name}'
    )
    return button


def get_zmanim_settings_keyboard(zmanim_data: dict) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    row = []

    for name, status in zmanim_data.items():
        row.append(get_zman_button(name, status))
        if sum([len(button.text) for button in row]) > 30:
            kb.row(*row)
            row = []

    return kb


def get_report_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(buttons.cancel.value, buttons.done.value)
    return kb
