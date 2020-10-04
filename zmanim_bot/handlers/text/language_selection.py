from aiogram.types import Message

from ...misc import dp
from ...config import LANGUAGE_LIST, LANGUAGE_SHORTCUTS
from ...api import get_or_set_lang
from ...handlers.redirects import redirect_to_main_menu
from ...middlewares.i18n import i18n_
from ...tracking import track


@dp.message_handler(text=LANGUAGE_LIST)
@track('Language selected', attach_message_text=True)
async def language_handler(msg: Message):
    lang = LANGUAGE_SHORTCUTS[msg.text]
    await get_or_set_lang(lang)
    i18n_.ctx_locale.set(lang)
    return await redirect_to_main_menu()
