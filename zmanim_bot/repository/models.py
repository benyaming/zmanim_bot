from datetime import datetime as dt
from typing import List, Optional, Tuple

from odmantic import EmbeddedModel, Field, Model

from zmanim_bot.config import config
from zmanim_bot.exceptions import NoLocationException, UnknownProcessorException
from zmanim_bot.processors import PROCESSORS
from zmanim_bot.processors.base import BaseProcessor

HAVDALA_OPINIONS = ['tzeis_5_95_degrees', 'tzeis_8_5_degrees', 'tzeis_42_minutes', 'tzeis_72_minutes']


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
    elevation: int | None = 0

    @property
    def coordinates(self) -> Tuple[float, float, int]:
        return self.lat, self.lng, self.elevation


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

