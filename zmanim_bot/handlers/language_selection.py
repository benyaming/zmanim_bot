from aiogram.types import Message

from ..misc import dp
from ..config import LANGUAGE_LIST, LANGUAGE_SHORTCUTS
from ..storage import get_or_set_lang
from .redirects import redirect_to_main_menu


@dp.message_handler(text=LANGUAGE_LIST)
async def language_handler(msg: Message):
    lang = LANGUAGE_SHORTCUTS[msg.text]
    await get_or_set_lang(lang)
    return await redirect_to_main_menu()
