from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from aiogram.types import InlineKeyboardMarkup

from zmanim_bot.integrations.zmanim_models import (Zmanim, Shabbat, YomTov, Fast, IsraelHolidays, RoshChodesh, DafYomi,
                                                   Holiday)

PROCESSORS = dict()


class BaseProcessor(ABC):
    _type: str
    _location_name: str

    def __init__(self, location_name: str):
        self._location_name = location_name

    def __init_subclass__(cls, **kwargs):
        PROCESSORS[cls._type] = cls

    @abstractmethod
    async def _send(self, data: ..., kb: Optional[InlineKeyboardMarkup] = None):
        ...

    async def send_zmanim(self, data: Zmanim):
        await self._send(self._get_zmanim(data))

    async def send_shabbat(self, data: Shabbat):
        await self._send(self._get_shabbat(data))

    async def send_yom_tov(self, data: YomTov):
        await self._send(self._get_yom_tov(data))

    async def send_fast(self, data: Fast):
        await self._send(self._get_fast(data))

    async def send_holiday(self, data: Holiday):
        await self._send(self._get_holiday(data))

    async def send_israel_holidays(self, data: IsraelHolidays):
        await self._send(self._get_israel_holidays(data))

    async def send_rosh_chodesh(self, data: RoshChodesh):
        await self._send(self._get_rosh_chodesh(data))

    async def send_daf_yomi(self, data: DafYomi):
        await self._send(self._get_daf_yomi(data))

    @abstractmethod
    def _get_zmanim(self, data: Zmanim):
        ...

    @abstractmethod
    def _get_shabbat(self, data: Shabbat):
        ...

    @abstractmethod
    def _get_yom_tov(self, data: YomTov):
        ...

    @abstractmethod
    def _get_fast(self, data: Fast):
        ...

    @abstractmethod
    def _get_holiday(self, data: Holiday):
        ...

    @abstractmethod
    def _get_israel_holidays(self, data: IsraelHolidays):
        ...

    @abstractmethod
    def _get_rosh_chodesh(self, data: RoshChodesh):
        ...

    @abstractmethod
    def _get_daf_yomi(self, data: DafYomi):
        ...
