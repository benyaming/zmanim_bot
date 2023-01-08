from abc import abstractmethod
from datetime import datetime as dt, timedelta
from enum import Enum

from pydantic import BaseModel
from zmanim.hebrew_calendar.jewish_calendar import JewishDate

from zmanim_bot.integrations.zmanim_api_client import get_zmanim


class TriggerType(Enum):
    gregorian_date = 'gregorian_date'
    hebrew_date = 'hebrew_date'
    zman = 'zman'


class ZmanType(Enum):
    alos = 'alos'
    misheyakir_10_2 = 'misheyakir_10_2'
    sunrise = 'sunrise'
    sof_zman_shema_ma = 'sof_zman_shema_ma'
    sof_zman_shema_gra = 'sof_zman_shema_gra'
    sof_zman_tefila_ma = 'sof_zman_tefila_ma'
    sof_zman_tefila_gra = 'sof_zman_tefila_gra'
    chatzos = 'chatzos'
    mincha_gedola = 'mincha_gedola'
    mincha_ketana = 'mincha_ketana'
    plag_mincha = 'plag_mincha'
    sunset = 'sunset'
    tzeis_5_95_degrees = 'tzeis_5_95_degrees'
    tzeis_8_5_degrees = 'tzeis_8_5_degrees'
    tzeis_42_minutes = 'tzeis_42_minutes'
    tzeis_72_minutes = 'tzeis_72_minutes'
    chatzot_laila = 'chatzot_laila'


class EventTrigger(BaseModel):

    @abstractmethod
    def calculate_next_event_dt(self, from_point: dt | None = None) -> dt:
        raise NotImplemented()


class GregorianDateTrigger(EventTrigger):
    """
    A trigger that executes on each gregorian date every year
    """

    month: int
    day: int
    hour: int
    minute: int

    def calculate_next_event_dt(self, from_point: dt | None = None) -> dt:
        if not from_point:
            from_point = dt.now()

        next_event = dt(
            year=from_point.year,
            month=self.month,
            day=self.day,
            hour=self.hour,
            minute=self.minute
        )
        if next_event < from_point:
            next_event = dt(
                year=from_point.year + 1,
                month=self.month,
                day=self.day,  # todo: days in month less then in previous year?
                hour=self.hour,
                minute=self.minute
            )
        return next_event


class JewishDateTrigger(EventTrigger):
    """
    A trigger that executes on each jewish date every year
    """

    j_month: int
    j_day: int
    hour: int
    minute: int

    def calculate_next_event_dt(self, from_point: dt | None = None) -> dt:
        if not from_point:
            from_point = dt.now()

        j_from_point = JewishDate.from_date(from_point.date())

        next_event_j_date = JewishDate(
            j_from_point.jewish_year,
            self.j_month,
            self.j_day
        )
        if next_event_j_date < j_from_point:
            next_event_j_date = JewishDate(
                j_from_point.jewish_year + 1,  # todo: adar ii?
                self.j_month,  # todo: days in month less then in previous year?
                self.j_day
            )

        next_event_date = next_event_j_date.gregorian_date
        next_event = dt(
            year=next_event_date.year,
            month=next_event_date.month,
            day=next_event_date.day,
            hour=self.hour,
            minute=self.minute
        )
        return next_event


class ZmanTrigger(EventTrigger):
    """
    A trigger that executes each day at selected zman
    """
    zman_type: ZmanType
    user_lat: float
    user_lng: float

    async def __get_zman(self, date_: str) -> dt:
        zmanim = await get_zmanim(
            (self.user_lat, self.user_lng),
            {self.zman_type.value: True},
            date_
        )
        next_event = getattr(zmanim, self.zman_type.value)
        return next_event

    async def calculate_next_event_dt(self, from_point: dt | None = None) -> dt:
        if not from_point:
            from_point = dt.now()

        next_event = await self.__get_zman(from_point.date().isoformat())

        if next_event < from_point.replace(tzinfo=next_event.tzinfo):
            from_point += timedelta(days=1)
            next_event = await self.__get_zman(from_point.date().isoformat())

        # todo asur be-melacha?
        return next_event


# todo: candle light trigger
# todo: significant day trigger
