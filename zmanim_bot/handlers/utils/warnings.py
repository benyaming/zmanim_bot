from aiogram.types import User

import zmanim_bot.keyboards.menus
from zmanim_bot.misc import bot
from zmanim_bot.texts.single import messages

__all__ = [
    'incorrect_greg_date_warning',
    'incorrect_jew_date_warning'
]


async def incorrect_greg_date_warning():
    user_id = User.get_current().id
    kb = zmanim_bot.keyboards.menus.get_cancel_keyboard()
    await bot.send_message(user_id, messages.incorrect_greg_date, reply_markup=kb)


async def incorrect_jew_date_warning():
    user_id = User.get_current().id
    kb = zmanim_bot.keyboards.menus.get_cancel_keyboard()
    await bot.send_message(user_id, messages.incorrect_jew_date, reply_markup=kb)
