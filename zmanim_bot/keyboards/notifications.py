from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from zmanim_bot.helpers import CallbackPrefixes, ZmanimType


def add_notification_button_to_kb(kb: InlineKeyboardMarkup, feature_type: str) -> None:
    # todo translate
    kb.row(InlineKeyboardButton(
        text='🔔 Create notification',
        callback_data=f'{CallbackPrefixes.init_notification_setup}{feature_type}'
    ))


zmanim_notifications_kb = InlineKeyboardMarkup()

for zman_type in ZmanimType:
    zmanim_notifications_kb.row(
        InlineKeyboardButton(
            text=f'{zman_type.name}',
            callback_data=f'{CallbackPrefixes.select_notification_zmanim}{zman_type.value}'
        )
    )
