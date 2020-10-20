from aiogram.types import User

from ..keyboards import menus
from ..misc import bot

from ..texts.single import messages

__all__ = [
    'redirect_to_main_menu',
    'redirect_to_request_location',
    'redirect_to_request_language',
]


async def redirect_to_main_menu(text: str = None):
    user_id = User.get_current().id
    kb = menus.get_main_menu()
    await bot.send_message(user_id, text or messages.init_main_menu, reply_markup=kb)
    
    
async def redirect_to_request_location(with_back: bool = False):
    user_id = User.get_current().id
    kb = menus.get_geobutton(with_back)
    await bot.send_message(user_id, messages.request_location, reply_markup=kb)
    
    
async def redirect_to_request_language():
    user_id = User.get_current().id
    kb = menus.get_lang_menu()
    resp = messages.request_language.value
    if resp == 'request language':
        resp = 'Select your language:'
    await bot.send_message(user_id, resp, reply_markup=kb)
