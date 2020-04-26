from aiogram.types import User, Message

from .. import keyboards 
# from .. import texts as txt
from ..misc import bot
from ..storage import get_or_set_lang

from ..texts import messages


async def redirect_to_main_menu():
    user_id = User.get_current().id
    kb = keyboards.get_main_menu()
    await bot.send_message(user_id, messages.init_main_menu.value, reply_markup=kb)
    
    
async def redirect_to_request_location():
    user_id = User.get_current().id
    kb = keyboards.get_geobutton()
    await bot.send_message(user_id, messages.request_location, reply_markup=kb)
    
    
async def redirect_to_request_language():
    user_id = User.get_current().id
    kb = keyboards.get_lang_menu()
    await bot.send_message(user_id, messages.request_language, reply_markup=kb)


async def incorrect_text_warning():
    user_id = User.get_current().id
    await bot.send_message(user_id, messages.incorrect_text)
