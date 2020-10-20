from aiogram.types import User

import zmanim_bot.keyboards.menus
from .. import keyboards
from ..texts.single import messages
from ..misc import bot


__all__ = [
    # 'incorrect_text_warning',
    'incorrect_greg_date_warning',
    'incorrect_jew_date_warning'
]


# async def incorrect_text_warning():
#     user_id = User.get_current().id
#     await bot.send_message(user_id, messages.incorrect_text)


async def incorrect_greg_date_warning():
    user_id = User.get_current().id
    kb = zmanim_bot.keyboards.menus.get_cancel_keyboard()
    await bot.send_message(user_id, messages.incorrect_greg_date, reply_markup=kb)


async def incorrect_jew_date_warning():
    user_id = User.get_current().id
    kb = zmanim_bot.keyboards.menus.get_cancel_keyboard()
    await bot.send_message(user_id, messages.incorrect_jew_date, reply_markup=kb)
