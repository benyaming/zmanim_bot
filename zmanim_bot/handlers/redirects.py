from aiogram.types import User

import zmanim_bot.keyboards.menus
from .. import keyboards
from ..misc import bot

from ..texts.single import messages

__all__ = [
    'redirect_to_main_menu',
    'redirect_to_request_location',
    'redirect_to_request_language',
]


async def redirect_to_main_menu(text: str = None):
    user_id = User.get_current().id
    kb = zmanim_bot.keyboards.menus.get_main_menu()
    await bot.send_message(user_id, text or messages.init_main_menu, reply_markup=kb)
    
    
async def redirect_to_request_location(with_back: bool = False):
    user_id = User.get_current().id
    kb = zmanim_bot.keyboards.menus.get_geobutton(with_back)
    await bot.send_message(user_id, messages.request_location, reply_markup=kb)
    
    
async def redirect_to_request_language():
    user_id = User.get_current().id
    kb = zmanim_bot.keyboards.menus.get_lang_menu()
    await bot.send_message(user_id, messages.request_language, reply_markup=kb)

