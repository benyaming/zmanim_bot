from __future__ import annotations

from io import BytesIO
from typing import Optional

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, Message, User, CallbackQuery

from zmanim_bot.integrations.zmanim_models import *
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

    def _get_zmanim(self, data: Zmanim) -> BytesIO:
        return renderer.ZmanimImage(data, self._location_name).get_image()

    async def _get_shabbat(self, data: Shabbat):
        pass

    async def _get_yom_tov(self, data: YomTov):
        pass

    async def _get_fast(self, data: Fast):
        pass

    async def _get_holiday(self, data: Holiday):
        pass

    async def _get_israel_holidays(self, data: IsraelHolidays):
        pass

    async def _get_rosh_chodesh(self, data: RoshChodesh):
        pass

    async def _get_daf_yomi(self, data: DafYomi):
        pass
