from __future__ import annotations

from io import BytesIO
from typing import Optional, Tuple

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, Message, User, CallbackQuery

from zmanim_bot.integrations import zmanim_models
from zmanim_bot.processors.base import BaseProcessor
from zmanim_bot.processors.image import renderer


class ImageProcessor(BaseProcessor):

    _type = 'image'

    async def _send(self, image: BytesIO, kb: Optional[InlineKeyboardMarkup] = None):
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

        await bot.send_photo(user.id, image, reply_markup=kb, reply_to_message_id=reply_to)

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
