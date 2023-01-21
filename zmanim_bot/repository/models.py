from __future__ import annotations

from abc import abstractmethod
from datetime import datetime as dt, timedelta
from typing import List, Optional, Tuple

from odmantic import EmbeddedModel, Field, Model
from zmanim.hebrew_calendar.jewish_date import JewishDate

from zmanim_bot.config import config
from zmanim_bot.exceptions import NoLocationException, UnknownProcessorException
from zmanim_bot.integrations.zmanim_api_client import get_zmanim
from zmanim_bot.processors import PROCESSORS
from zmanim_bot.processors.base import BaseProcessor
from zmanim_bot.repository import bot_repository

HAVDALA_OPINIONS = ['tzeis_5_95_degrees', 'tzeis_8_5_degrees', 'tzeis_42_minutes', 'tzeis_72_minutes']

# todo refactor: split repositories!


class UserInfo(EmbeddedModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None


class UserMeta(EmbeddedModel):
    last_seen_at: dt = Field(default_factory=dt.now)
    is_banned_by_admin: bool = False
    is_user_blocked_bot: bool = False


class Location(EmbeddedModel):
    lat: float
    lng: float
    name: str
    is_active: bool

    @property
    def coordinates(self) -> Tuple[float, float]:
        return self.lat, self.lng


class OmerSettings(EmbeddedModel):
    is_enabled: bool = False
    is_sent_today: Optional[bool]
    notification_time: Optional[str]


class ZmanimSettings(EmbeddedModel):
    alos: bool = True
    misheyakir_10_2: bool = True
    sunrise: bool = True
    sof_zman_shema_ma: bool = False
    sof_zman_shema_gra: bool = True
    sof_zman_tefila_ma: bool = False
    sof_zman_tefila_gra: bool = True
    chatzos: bool = True
    mincha_gedola: bool = True
    mincha_ketana: bool = False
    plag_mincha: bool = False
    sunset: bool = True
    tzeis_5_95_degrees: bool = False
    tzeis_8_5_degrees: bool = True
    tzeis_42_minutes: bool = False
    tzeis_72_minutes: bool = False
    chatzot_laila: bool = False
    astronomical_hour_ma: bool = False
    astronomical_hour_gra: bool = False


class User(Model):
    user_id: int
    personal_info: UserInfo = Field(default_factory=UserInfo)

    language: Optional[str] = None
    location_list: List[Location] = Field(default_factory=list)
    cl_offset: int = 18
    havdala_opinion: str = 'tzeis_8_5_degrees'
    zmanim_settings: ZmanimSettings = Field(default_factory=ZmanimSettings)
    processor_type: str = 'image'
    omer: OmerSettings = Field(default_factory=OmerSettings)

    meta: UserMeta = Field(default_factory=UserMeta)

    class Config:
        collection = config.DB_COLLECTION_NAME
        parse_doc_with_default_factories = True

    @property
    def location(self) -> Location:
        loc = list(filter(lambda l: l.is_active, self.location_list))
        if not loc:
            raise NoLocationException
        return loc[0]

    def get_location_by_coords(self, lat: float, lng: float) -> Location:
        resp = list(filter(lambda loc: loc.lat == lat and loc.lng == lng, self.location_list))
        if not resp:
            raise NoLocationException
        return resp[0]

    def get_processor(self, location: Optional[Location] = None) -> BaseProcessor:
        try:
            return PROCESSORS[self.processor_type]((location and location.name) or self.location.name)
        except KeyError:
            raise UnknownProcessorException()


class Event(Model):
    owner_id: int
    name: str
    message: str
    trigger: GregorianDateTrigger | JewishDateTrigger | ZmanTrigger

    class Config:
        collection = 'events'


class EventTrigger(EmbeddedModel):
    type: str

    @abstractmethod
    def calculate_next_event_dt(
            self, from_point: dt | None = None,
            user_id: int | None = None
    ) -> dt:
        raise NotImplemented()


class GregorianDateTrigger(EventTrigger):
    """
    A trigger that executes on each gregorian date every year
    """
    # todo user's timezone?

    month: int
    day: int
    hour: int
    minute: int

    def calculate_next_event_dt(self, from_point: dt | None = None, _=None) -> dt:
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
    # todo user's timezone?

    j_month: int
    j_day: int
    hour: int
    minute: int

    def calculate_next_event_dt(self, from_point: dt | None = None, _=None) -> dt:
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
    zman_type: str
    type: str = 'ZmanTrigger'
    offset: int  # todo missing implementation

    async def __get_zman(self, date_: str, user_id: int) -> dt:
        user = await bot_repository.get_user_by_id(user_id)
        zmanim = await get_zmanim(
            (user.location.lat, user.location.lng),
            {self.zman_type: True},
            date_
        )
        next_event = getattr(zmanim, self.zman_type)
        return next_event

    async def calculate_next_event_dt(
            self,
            from_point: dt | None = None,
            user_id: int | None = None
    ) -> dt:
        if not user_id:
            raise ValueError('No user_id was provided!')
        if not from_point:
            from_point = dt.now()

        next_event = await self.__get_zman(from_point.date().isoformat(), user_id)

        if next_event < from_point.replace(tzinfo=next_event.tzinfo):
            from_point += timedelta(days=1)
            next_event = await self.__get_zman(from_point.date().isoformat(), user_id)

        # todo asur be-melacha?
        return next_event


Event.update_forward_refs()


# todo: candle light trigger
# todo: significant day trigger
