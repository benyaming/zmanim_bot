from aiogram.types import User

from zmanim_bot.config import config
from zmanim_bot.keyboards import menus, inline
from zmanim_bot.miniapp import build_miniapp_url, update_menu_button
from zmanim_bot.misc import bot
from zmanim_bot.repository.bot_repository import get_or_create_user
from zmanim_bot.texts.single import messages

__all__ = [
    'redirect_to_main_menu',
    'redirect_to_settings_menu',
    'redirect_to_request_location',
    'redirect_to_request_language',
]


async def redirect_to_main_menu(text: str = None):
    user_id = User.get_current().id
    # Every return to the main menu re-personalizes the mini-app entry points
    # (keyboard button + chat menu button), so a location or language change
    # made in the bot is reflected in the next launch URL.
    miniapp_url = None
    if config.MINIAPP_URL:
        miniapp_url = build_miniapp_url(await get_or_create_user())
        await update_menu_button(user_id, miniapp_url)
    kb = menus.get_main_menu(miniapp_url)
    await bot.send_message(user_id, text or messages.init_main_menu, reply_markup=kb)


async def redirect_to_settings_menu(text: str = None):
    user_id = User.get_current().id
    kb = menus.get_settings_menu()
    await bot.send_message(user_id, text or messages.init_main_menu, reply_markup=kb)
    
    
async def redirect_to_request_location():
    user_id = User.get_current().id
    kb = inline.LOCATION_SEARCH_KB
    await bot.send_message(user_id, messages.request_location_on_init, reply_markup=kb)
    
    
async def redirect_to_request_language():
    user_id = User.get_current().id
    kb = menus.get_lang_menu()
    resp = messages.request_language.value
    if resp == 'request language':
        resp = 'Select your language:'
    await bot.send_message(user_id, resp, reply_markup=kb)
