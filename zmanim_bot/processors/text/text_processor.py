from typing import Tuple

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, User, CallbackQuery, Message

from zmanim_bot.integrations.zmanim_models import DafYomi, RoshChodesh, IsraelHolidays, Holiday, \
    Fast, YomTov, Shabbat, Zmanim
from zmanim_bot.keyboards import inline
from zmanim_bot.processors import BaseProcessor
from zmanim_bot.processors.text import composer


class TextProcessor(BaseProcessor[str]):

    _type = 'text'

    async def _send(self, text: str, *kb_list: InlineKeyboardMarkup):
        bot = Bot.get_current()
        user = User.get_current()
        call = CallbackQuery.get_current()
        message = Message.get_current()
        kb_list = [kb for kb in kb_list if kb]  # clean from None

        if call:
            reply_to = call.message.message_id
        elif message:
            reply_to = message and message.message_id
        else:
            reply_to = None

        if len(kb_list) == 0:
            kb = None
        elif len(kb_list) == 1:
            kb = kb_list[0]
        else:
            kb = inline.merge_inline_keyboards(kb_list[0], kb_list[1])

        await bot.send_message(user.id, text, reply_markup=kb, reply_to_message_id=reply_to)

    async def _update(self, text: str, *kb_list: InlineKeyboardMarkup):
        bot = Bot.get_current()
        user = User.get_current()
        call = CallbackQuery.get_current()
        kb_list = [kb for kb in kb_list if kb]  # clean from None

        if len(kb_list) == 0:
            kb = None
        elif len(kb_list) == 1:
            kb = kb_list[0]
        else:
            kb = inline.merge_inline_keyboards(kb_list[0], kb_list[1])

        await bot.edit_message_text(text, user.id, call.message.message_id, reply_markup=kb)

    def _get_zmanim(self, data: Zmanim) -> str:
        return composer.compose_zmanim(data, self._location_name)

    def _get_shabbat(self, data: Shabbat) -> Tuple[str, InlineKeyboardMarkup]:
        return composer.compose_shabbat(data, self._location_name)

    def _get_yom_tov(self, data: YomTov) -> Tuple[str, InlineKeyboardMarkup]:
        pass

    def _get_fast(self, data: Fast) -> Tuple[str, InlineKeyboardMarkup]:
        pass

    def _get_holiday(self, data: Holiday) -> str:
        pass

    def _get_israel_holidays(self, data: IsraelHolidays) -> str:
        pass

    def _get_rosh_chodesh(self, data: RoshChodesh) -> str:
        pass

    def _get_daf_yomi(self, data: DafYomi) -> str:
        pass
