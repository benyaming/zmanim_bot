from datetime import date
from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..processors.text_utils import humanize_date
from ..texts.single import zmanim
from ..texts.single import messages
from ..helpers import CL_OFFET_OPTIONS, HAVDALA_OPINION_OPTIONS, CallbackPrefixes
from ..texts.single.buttons import zmanim_for


def get_cl_settings_keyboard(current_value: int) -> InlineKeyboardMarkup:
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


def get_havdala_settings_keyboard(current_value: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    for option in HAVDALA_OPINION_OPTIONS:
        option_name = getattr(zmanim, option)
        button = InlineKeyboardButton(
            text=f'{option_name}' if option != current_value else f'✅ {option_name}',
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

    for name, status in zmanim_data.items():
        row = [get_zman_button(name, status)]
        kb.row(*row)

    return kb


def get_omer_kb(status: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton(
            text=f'✅   {messages.settings_enabled}' if status
            else f'❌   {messages.settings_disabled}',
            callback_data=f'{CallbackPrefixes.omer}{int(status)}'
        )
    )
    return kb


def get_zmanim_by_date_buttons(dates: List[date]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for d in dates:
        kb.row(InlineKeyboardButton(
            text=f'{zmanim_for} {humanize_date([d])}',
            callback_data=f'{CallbackPrefixes.zmanim_by_date}{d.isoformat()}'
        ))
    return kb
