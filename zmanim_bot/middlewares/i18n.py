from pathlib import Path
from typing import Any, Tuple

from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram.types import Message

from zmanim_bot.config import config

LOCALES_DIR = Path(__file__).parent.parent.parent / 'locales'


class I18N(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        if isinstance(args[0], Message) and args[0].chat.type == 'channel':
            return ''

        if len(args) > 0 and isinstance(args[0], Message) and args[0].text in config.LANGUAGE_LIST:
            locale = args[0].text
        else:
            from zmanim_bot.repository.bot_repository import get_or_set_lang

            locale = await get_or_set_lang()

        return locale

    def is_rtl(self) -> bool:
        return self.ctx_locale.get() == 'he'


i18n_ = I18N(config.I18N_DOMAIN, LOCALES_DIR)
gettext = i18n_.gettext
lazy_gettext = i18n_.lazy_gettext
