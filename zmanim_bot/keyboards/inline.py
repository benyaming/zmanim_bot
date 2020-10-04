from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..texts.single import zmanim
from ..helpers import CL_OFFET_OPTIONS, HAVDALA_OPINION_OPTIONS, CallbackPrefixes


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


def get_zmanim_settings_keyboard(zmanim_data: dict) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    # row = []

    for name, status in zmanim_data.items():
        row = [get_zman_button(name, status)]
        kb.row(*row)
        # if sum([len(button.text) for button in row]) > 30:
        #     kb.row(*row)
        #     row = []

    return kb


def get_zman_button(name: str, status: bool) -> InlineKeyboardButton:
    button = InlineKeyboardButton(
        text=f'{"✅" if status else "❌"} {getattr(zmanim, name)}',
        callback_data=f'{CallbackPrefixes.zmanim}{name}'
    )
    return button
