from __future__ import annotations
from typing import List, Optional, Tuple, Dict
from datetime import datetime, time, date

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
    'Zmanim'
]


class SimpleSettings(BaseModel):
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


class Zmanim(BaseModel):
    settings: Settings
    sunrise: Optional[datetime] = None
    alos: Optional[datetime] = None
    sof_zman_tefila_gra: Optional[datetime] = None
    sof_zman_tefila_ma: Optional[datetime] = None
    talis_ma: Optional[datetime] = None
    sof_zman_shema_gra: Optional[datetime] = None
    mincha_ketana: Optional[datetime] = None
    sof_zman_shema_ma: Optional[datetime] = None
    chatzos: Optional[datetime] = None
    mincha_gedola: Optional[datetime] = None
    plag_mincha: Optional[datetime] = None
    sunset: Optional[datetime] = None
    tzeis_8_5_degrees: Optional[datetime] = None
    tzeis_72_minutes: Optional[datetime] = None
    tzeis_42_minutes: Optional[datetime] = None
    tzeis_5_95_degrees: Optional[datetime] = None
    chatzot_laila: Optional[datetime] = None
    astronomical_hour_ma: Optional[time] = None
    astronomical_hour_gra: Optional[time] = None


class AsurBeMelachaDay(BaseModel):
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


IsraelHolidays = List[Dict[str, date]]


class YomTov(BaseModel):
    settings: Settings
    pre_shabbat: Optional[AsurBeMelachaDay] = None
    day_1: AsurBeMelachaDay
    day_2: Optional[AsurBeMelachaDay] = None
    post_shabbat: Optional[AsurBeMelachaDay] = None
    hoshana_rabba: Optional[date] = None

    pesach_part_2_day_1: Optional[AsurBeMelachaDay] = None
    pesach_part_2_day_2: Optional[AsurBeMelachaDay] = None


class Fast(BaseModel):
    settings: Settings
    moved_fast: Optional[bool] = False
    fast_start: Optional[datetime] = None
    chatzot: Optional[datetime] = None
    havdala: Optional[datetime] = None
