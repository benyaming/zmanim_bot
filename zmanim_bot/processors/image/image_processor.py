from __future__ import annotations

from io import BytesIO
from typing import Tuple

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, Message, User, CallbackQuery, InputMedia

from zmanim_bot.integrations import zmanim_models
from zmanim_bot.keyboards import inline
from zmanim_bot.processors.base import BaseProcessor
from zmanim_bot.processors.image import renderer


class ImageProcessor(BaseProcessor[BytesIO]):

    _type = 'image'

    async def _send(self, image: BytesIO, *kb_list: InlineKeyboardMarkup):
        bot = Bot.get_current()
        user = User.get_current()
        call = CallbackQuery.get_current()
        message = Message.get_current()

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

        await bot.send_photo(user.id, image, reply_markup=kb, reply_to_message_id=reply_to)

    async def _update(self, image: BytesIO, *kb_list: InlineKeyboardMarkup):
        bot = Bot.get_current()
        user = User.get_current()
        call = CallbackQuery.get_current()

        media = InputMedia(media=image)

        if len(kb_list) == 0:
            kb = None
        elif len(kb_list) == 1:
            kb = kb_list[0]
        else:
            kb = inline.merge_inline_keyboards(kb_list[0], kb_list[1])

        await bot.edit_message_media(media, user.id, call.message.message_id, reply_markup=kb)

    def _get_zmanim(self, data: zmanim_models.Zmanim) -> BytesIO:
        return renderer.ZmanimImage(data, self._location_name).get_image()

    def _get_shabbat(self, data: zmanim_models.Shabbat) -> Tuple[BytesIO, InlineKeyboardMarkup]:
        return renderer.ShabbatImage(data, self._location_name).get_image()

    def _get_yom_tov(self, data: zmanim_models.YomTov) -> Tuple[BytesIO, InlineKeyboardMarkup]:
        return renderer.YomTovImage(data, self._location_name).get_image()

    def _get_fast(self, data: zmanim_models.Fast) -> Tuple[BytesIO, InlineKeyboardMarkup]:
        return renderer.FastImage(data, self._location_name).get_image()

    def _get_holiday(self, data: zmanim_models.Holiday) -> BytesIO:
        return renderer.HolidayImage(data).get_image()

    def _get_israel_holidays(self, data: zmanim_models.IsraelHolidays) -> BytesIO:
        return renderer.IsraelHolidaysImage(data).get_image()

    def _get_rosh_chodesh(self, data: zmanim_models.RoshChodesh) -> BytesIO:
        return renderer.RoshChodeshImage(data).get_image()

    def _get_daf_yomi(self, data: zmanim_models.DafYomi) -> BytesIO:
        return renderer.DafYomImage(data).get_image()
