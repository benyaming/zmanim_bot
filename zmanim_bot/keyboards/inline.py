from datetime import date
from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from zmanim_bot.repository.bot_repository import Location
from zmanim_bot.processors.text_utils import humanize_date
from zmanim_bot.texts.single import zmanim, buttons
from zmanim_bot.helpers import CL_OFFET_OPTIONS, HAVDALA_OPINION_OPTIONS, CallbackPrefixes
from zmanim_bot.texts.single.buttons import zmanim_for_date_prefix


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
            text=f'✅   {buttons.settings_enabled}' if status
            else f'❌   {buttons.settings_disabled}',
            callback_data=f'{CallbackPrefixes.omer}{int(status)}'
        )
    )
    return kb


def get_zmanim_by_date_buttons(dates: List[date]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for d in dates:
        kb.row(InlineKeyboardButton(
            text=f'{zmanim_for_date_prefix} {humanize_date([d])}',
            callback_data=f'{CallbackPrefixes.zmanim_by_date}{d.isoformat()}'
        ))
    return kb


def get_location_options_menu(location_list: List[Location]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    for location in location_list:
        status = '🔘' if location.is_active else '⚪️'
        kb.row(InlineKeyboardButton(
            text=f'{status} {location.name}',
            callback_data=f'{CallbackPrefixes.location_activate}{location.name}'
        ))
        kb.row(
            InlineKeyboardButton(text='✏️', callback_data=f'{CallbackPrefixes.location_rename}{location.name}'),
            InlineKeyboardButton(text='❌', callback_data=f'{CallbackPrefixes.location_delete}{location.name}')
        )

    return kb
