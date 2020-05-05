from pydantic import BaseModel
from datetime import time, datetime, date
from typing import Tuple, List


class ZmanimApiZmmanim(BaseModel):
    sunrise: time = None
    alos: time = None
    sof_zman_tefila_gra: time = None
    sof_zman_tefila_ma: time = None
    talis_ma: time = None
    sof_zman_shema_gra: time = None
    sof_zman_shema_ma: time = None
    chatzos: time = None
    mincha_ketana: time = None
    mincha_gedola: time = None
    plag_mincha: time = None
    sunset: time = None
    tzeis_8_5_degrees: time = None
    tzeis_72_minutes: time = None
    tzeis_42_minutes: time = None
    tzeis_5_95_degrees: time = None
    chatzot_laila: time = None


class ZmanimApiShabbos(BaseModel):
    torah_part: str = None
    cl: datetime = None
    cl_offset: int = None
    havdala: datetime = None
    havdala_opinion: str = None
    late_cl_warning: bool = None


class ZmanimApiDafYomi(BaseModel):
    masehet: str = None
    daf: int = None


class ZmanimApiRoshChodesh(BaseModel):
    month_name: str = None
    days: List[date] = None
    duration: int = None
    molad: Tuple[datetime, int]
