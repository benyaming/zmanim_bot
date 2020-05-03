from aiogram.types import Message

from zmanim_bot.misc import dp
from zmanim_bot.config import LANGUAGE_LIST, LANGUAGE_SHORTCUTS
from zmanim_bot.api import get_or_set_lang
from zmanim_bot.handlers.redirects import redirect_to_main_menu


@dp.message_handler(text=LANGUAGE_LIST)
async def language_handler(msg: Message):
    lang = LANGUAGE_SHORTCUTS[msg.text]
    await get_or_set_lang(lang)
    return await redirect_to_main_menu()
