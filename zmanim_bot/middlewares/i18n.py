from pathlib import Path
from typing import Tuple, Any

from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram.types import Message

from zmanim_bot.misc import dp
from zmanim_bot.repository.bot_repository import get_or_set_lang
from zmanim_bot.config import I18N_DOMAIN, LANGUAGE_LIST


LOCALES_DIR = Path(__file__).parent.parent / 'locales'


class I18N(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        if isinstance(args[0], Message) and args[0].chat.type == 'channel':
            return ''

        if len(args) > 0 and isinstance(args[0], Message) and args[0].text in LANGUAGE_LIST:
            locale = args[0].text
        else:
            locale = await get_or_set_lang()

        return locale


i18n_ = I18N(I18N_DOMAIN, LOCALES_DIR)
dp.middleware.setup(i18n_)
gettext = i18n_.gettext
lazy_gettext = i18n_.lazy_gettext

# cd .\zmanim_bot\texts\single\
#  pybabel extract ..\plural\units.py .\buttons.py .\headers.py .\helpers.py .\messages.py .\names.py .\zmanim_api.py  -o .\..\..\locales\zmanim_bot.pot -k __:1,2

# pybabel init -i .\locales\zmanim_bot.pot -d .\locales\ -D zmanim_bot -l ru
# pybabel compile -d ..\..\locales\ -D zmanim_bot
