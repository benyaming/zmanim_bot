from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple, Generic, TypeVar

from aiogram.types import InlineKeyboardMarkup

from zmanim_bot.integrations.zmanim_models import (Zmanim, Shabbat, YomTov, Fast, IsraelHolidays,
                                                   RoshChodesh, DafYomi,
                                                   Holiday)

T = TypeVar('T')


class BaseProcessor(ABC, Generic[T]):
    _location_name: str

    def __init__(self, location_name: str):
        self._location_name = location_name

    @abstractmethod
    async def _send(self, data: T, *kb: InlineKeyboardMarkup):
        pass

    @abstractmethod
    async def _update(self, data: T, *kb: InlineKeyboardMarkup):
        pass

    async def send_zmanim(self, data: Zmanim, kb: InlineKeyboardMarkup):
        await self._send(self._get_zmanim(data), kb)

    async def send_shabbat(self, data: Shabbat, kb: InlineKeyboardMarkup):
        await self._send(*self._get_shabbat(data), kb)

    async def send_yom_tov(self, data: YomTov):
        await self._send(*self._get_yom_tov(data))

    async def send_fast(self, data: Fast, kb: InlineKeyboardMarkup):
        await self._send(*self._get_fast(data), kb)

    async def send_holiday(self, data: Holiday):
        await self._send(self._get_holiday(data))

    async def send_israel_holidays(self, data: IsraelHolidays):
        await self._send(self._get_israel_holidays(data))

    async def send_rosh_chodesh(self, data: RoshChodesh):
        await self._send(self._get_rosh_chodesh(data))

    async def send_daf_yomi(self, data: DafYomi):
        await self._send(self._get_daf_yomi(data))

    async def update_zmanim(self, data: Zmanim, kb: InlineKeyboardMarkup):
        await self._update(self._get_zmanim(data), kb)

    async def update_shabbat(self, data: Shabbat, kb: InlineKeyboardMarkup):
        await self._update(*self._get_shabbat(data), kb)

    async def update_yom_tov(self, data: YomTov, kb: InlineKeyboardMarkup):
        await self._update(*self._get_yom_tov(data), kb)

    async def update_fast(self, data: Fast, kb: InlineKeyboardMarkup):
        await self._update(*self._get_fast(data), kb)

    @abstractmethod
    def _get_zmanim(self, data: Zmanim) -> Tuple[T, InlineKeyboardMarkup]:
        pass

    @abstractmethod
    def _get_shabbat(self, data: Shabbat) -> Tuple[T, InlineKeyboardMarkup]:
        pass

    @abstractmethod
    def _get_yom_tov(self, data: YomTov) -> Tuple[T, InlineKeyboardMarkup]:
        pass

    @abstractmethod
    def _get_fast(self, data: Fast) -> Tuple[T, InlineKeyboardMarkup]:
        pass

    @abstractmethod
    def _get_holiday(self, data: Holiday) -> T:
        pass

    @abstractmethod
    def _get_israel_holidays(self, data: IsraelHolidays) -> T:
        pass

    @abstractmethod
    def _get_rosh_chodesh(self, data: RoshChodesh) -> T:
        pass

    @abstractmethod
    def _get_daf_yomi(self, data: DafYomi) -> T:
        pass
