from pathlib import Path
from typing import Tuple, Any

from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram.types import Message

from ..exceptions import NoLanguageException
from ..misc import dp
from ..api import get_or_set_lang
from ..config import I18N_DOMAIN, LANGUAGE_LIST


LOCALES_DIR = Path(__file__).parent.parent / 'locales'


class I18N(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        if isinstance(args[0], Message) and args[0].chat.type == 'channel':
            return ''

        locale = await get_or_set_lang()

        if not locale:
            if len(args) > 0 and isinstance(args[0], Message):

                if args[0].text in LANGUAGE_LIST:
                    locale = args[0].text
                elif args[0].text == '/start':
                    locale = ''
            else:
                raise NoLanguageException

        return locale


i18n_ = I18N(I18N_DOMAIN, LOCALES_DIR)
dp.middleware.setup(i18n_)
gettext = i18n_.gettext
lazy_gettext = i18n_.lazy_gettext

# cd .\zmanim_bot\texts\single\
#  pybabel extract ..\plural\units.py .\buttons.py .\headers.py .\helpers.py .\messages.py .\names.py .\zmanim.py  -o .\..\..\locales\zmanim_bot.pot

# pybabel init -i .\locales\zmanim_bot.pot -d .\locales\ -D zmanim_bot -l ru
# pybabel compile -d .\locales\ -D zmanim_bot
