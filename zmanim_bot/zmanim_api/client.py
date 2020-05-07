from typing import Type, TypeVar

from ..misc import bot
from ..api import Location
from . import models
from ..config import ZMANIM_API_URL


__all__ = [
    'get_zmanim',
    'get_shabbat',
    'get_daf_yomi',
    'get_rosh_chodesh',
    'get_holiday'
]

# T = TypeVar('T')
#
# async def _process_request(url, method: str = 'get', params: dict = None, body: dict = None,
#                            content_type: Type[T] = None) -> T:
#     async with getattr(bot.session, method)(url=url, params=params, json=body) as resp:
#         raw_resp = await resp.json()
#         resp = T(**raw_resp)
#         return resp


async def get_zmanim(location: Location, zmanim_settings: dict, date: str = None) -> models.ZmanimApiZmmanim:
    url = ZMANIM_API_URL.format('zmanim')
    params = {
        'lat': str(location[0]),
        'lng': str(location[1]),
    }
    if date:
        params['date'] = date

    async with bot.session.post(url, params=params, json=zmanim_settings) as resp:
        raw_resp = await resp.json()
        return models.ZmanimApiZmmanim(**raw_resp)


async def get_shabbat(location: Location, cl_offset: int, havdala_opinion: str,
                      date: str = None) -> models.ZmanimApiShabbos:
    url = ZMANIM_API_URL.format('shabbos')
    params = {
        'lat': str(location[0]),
        'lng': str(location[1]),
        'cl_offset': str(cl_offset),
        'havdala': havdala_opinion
    }
    if date:
        params['date'] = date

    async with bot.session.get(url, params=params) as resp:
        raw_resp = await resp.json()
        return models.ZmanimApiShabbos(**raw_resp)


async def get_daf_yomi(date=None) -> models.ZmanimApiDafYomi:
    url = ZMANIM_API_URL.format('daf_yomi')
    params = None if not date else {'date': date}

    async with bot.session.get(url, params=params) as resp:
        raw_resp = await resp.json()
        return models.ZmanimApiDafYomi(**raw_resp)


async def get_rosh_chodesh(date=None) -> models.ZmanimApiRoshChodesh:
    url = ZMANIM_API_URL.format('rosh_chodesh')
    params = None if not date else {'date': date}

    async with bot.session.get(url, params=params) as resp:
        raw_resp = await resp.json()
        return models.ZmanimApiRoshChodesh(**raw_resp)


async def get_holiday(name: str, cl_offset: int, havdala_opinion: str,
                      location: Location = None) -> models.ZmanimApiHoliday:
    url = ZMANIM_API_URL.format('holidays')
    params = {
        'lat': str(location[0]) if location else None,
        'lng': str(location[1]) if location else None,
        'holiday_name': name,
        'cl': str(cl_offset),
        'havdala': havdala_opinion
    }

    async with bot.session.get(url, params=params) as resp:
        raw_resp = await resp.json()
        return models.ZmanimApiHoliday(**raw_resp)

