from pathlib import Path
from typing import Tuple, Any

from aiogram.contrib.middlewares.i18n import I18nMiddleware

from ..misc import dp
from ..api import get_or_set_lang
from ..config import I18N_DOMAIN


LOCALES_DIR = Path(__file__).parent.parent / 'locales'


class I18N(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        return await get_or_set_lang()


i18n_ = I18N(I18N_DOMAIN, LOCALES_DIR)
dp.middleware.setup(i18n_)
gettext = i18n_.gettext
lazy_gettext = i18n_.lazy_gettext


# pybabel extract .\texts\buttons.py .\texts\messages.py -o .\locales\zmanim_bot.pot
# pybabel init -i .\locales\zmanim_bot.pot -d .\locales\ -D zmanim_bot -l ru
# pybabel compile -d .\locales\ -D zmanim_bot
