from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import List, Optional, Tuple

from pydantic import BaseModel

__all__ = [
    'Settings',
    'SimpleSettings',
    'AsurBeMelachaDay',
    'DafYomi',
    'RoshChodesh',
    'Shabbat',
    'YomTov',
    'Holiday',
    'Fast',
    'Zmanim',
    'IsraelHolidays'
]


class BaseModelWithZmanimLehumra(BaseModel):

    @staticmethod
    def _round_time_lehumra(dt: datetime, to_min: bool = False) -> datetime:
        delta = timedelta(minutes=1 if not to_min else -1)
        return dt + delta

    def apply_zmanim_lehumra(self):
        for name, value in self.dict(exclude={'settings'}).items():
            if isinstance(value, datetime):
                lehumra_minus_minute_names = [
                    'sof_zman_shema_ma', 'sof_zman_shema_gra', 'sof_zman_tefila_ma',
                    'sof_zman_tefila_gra', 'sunset', 'candle_lighting', 'fast_start'
                ]
                value_lehumra = self._round_time_lehumra(value, to_min=name in lehumra_minus_minute_names)
                setattr(self, name, value_lehumra)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apply_zmanim_lehumra()


class SimpleSettings(BaseModelWithZmanimLehumra):
    date_: Optional[date] = None
    jewish_date: Optional[str] = None
    holiday_name: Optional[str] = None

    class Config:
        fields = {'date_': 'date'}


class Settings(SimpleSettings):
    cl_offset: Optional[int] = None
    havdala_opinion: Optional[str] = None
    coordinates: Optional[Tuple[float, float]] = None
    elevation: Optional[int] = None
    fast_name: Optional[str] = None
    yomtov_name: Optional[str] = None


class Zmanim(BaseModelWithZmanimLehumra):
    settings: Settings
    alos: Optional[datetime] = None
    misheyakir_10_2: Optional[datetime] = None
    sunrise: Optional[datetime] = None
    sof_zman_shema_ma: Optional[datetime] = None
    sof_zman_shema_gra: Optional[datetime] = None
    sof_zman_tefila_ma: Optional[datetime] = None
    sof_zman_tefila_gra: Optional[datetime] = None
    chatzos: Optional[datetime] = None
    mincha_gedola: Optional[datetime] = None
    mincha_ketana: Optional[datetime] = None
    plag_mincha: Optional[datetime] = None
    sunset: Optional[datetime] = None
    tzeis_5_95_degrees: Optional[datetime] = None
    tzeis_8_5_degrees: Optional[datetime] = None
    tzeis_42_minutes: Optional[datetime] = None
    tzeis_72_minutes: Optional[datetime] = None
    chatzot_laila: Optional[datetime] = None
    astronomical_hour_ma: Optional[time] = None
    astronomical_hour_gra: Optional[time] = None


class AsurBeMelachaDay(BaseModelWithZmanimLehumra):
    date: Optional[date] = None
    candle_lighting: Optional[datetime] = None
    havdala: Optional[datetime] = None


class Shabbat(AsurBeMelachaDay):
    settings: Settings
    torah_part: str = None
    late_cl_warning: bool = False


class RoshChodesh(BaseModel):
    settings: SimpleSettings
    month_name: str
    days: List[date]
    duration: int
    molad: Tuple[datetime, int]

    class Config:
        json_encoders = {
            datetime: lambda d: d.isoformat(timespec='minutes')
        }


class DafYomi(BaseModel):
    settings: SimpleSettings
    masehet: str
    daf: int


class Holiday(BaseModel):
    settings: SimpleSettings
    date: date


class IsraelHolidays(BaseModel):
    settings: SimpleSettings
    holiday_list: List[Tuple[str, date]]


class YomTov(BaseModelWithZmanimLehumra):
    settings: Settings
    pre_shabbat: Optional[AsurBeMelachaDay] = None
    day_1: AsurBeMelachaDay
    day_2: Optional[AsurBeMelachaDay] = None
    post_shabbat: Optional[AsurBeMelachaDay] = None
    hoshana_rabba: Optional[date] = None

    pesach_part_2_day_1: Optional[AsurBeMelachaDay] = None
    pesach_part_2_day_2: Optional[AsurBeMelachaDay] = None


class Fast(BaseModelWithZmanimLehumra):
    settings: Settings
    moved_fast: Optional[bool] = False
    fast_start: Optional[datetime] = None
    chatzot: Optional[datetime] = None
    havdala_5_95_dgr: Optional[datetime] = None
    havdala_8_5_dgr: Optional[datetime] = None
    havdala_42_min: Optional[datetime] = None
