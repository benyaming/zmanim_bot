from datetime import date
from typing import Optional

from . import models
from .models import SimpleSettings
from zmanim_bot.misc import bot
from zmanim_bot.api.storage_api import Location
from zmanim_bot.config import ZMANIM_API_URL


__all__ = [
    'get_zmanim',
    'get_shabbat',
    'get_daf_yomi',
    'get_rosh_chodesh',
    'get_generic_yomtov',
    'get_generic_holiday',
    'get_generic_fast',
    'get_israel_holidays'
]


async def get_zmanim(location: Location, zmanim_settings: dict, date_: str = None) -> models.Zmanim:
    url = ZMANIM_API_URL.format('zmanim')
    params = {
        'lat': str(location[0]),
        'lng': str(location[1]),
    }
    if date_:
        params['date'] = date_

    async with bot.session.post(url, params=params, json=zmanim_settings) as resp:
        raw_resp = await resp.json()
        return models.Zmanim(**raw_resp)


async def get_shabbat(
        location: Location,
        cl_offset: int,
        havdala_opinion: str,
        date_: str = None
) -> models.Shabbat:
    url = ZMANIM_API_URL.format('shabbat')
    params = {
        'lat': str(location[0]),
        'lng': str(location[1]),
        'cl_offset': str(cl_offset),
        'havdala': havdala_opinion
    }
    if date_:
        params['date'] = date_

    async with bot.session.get(url, params=params) as resp:
        raw_resp = await resp.json()
        return models.Shabbat(**raw_resp)


async def get_daf_yomi(date_=None) -> models.DafYomi:
    url = ZMANIM_API_URL.format('daf_yomi')
    params = None if not date_ else {'date': date_}

    async with bot.session.get(url, params=params) as resp:
        raw_resp = await resp.json()
        return models.DafYomi(**raw_resp)


async def get_rosh_chodesh(date_=None) -> models.RoshChodesh:
    url = ZMANIM_API_URL.format('rosh_chodesh')
    params = None if not date_ else {'date': date_}

    async with bot.session.get(url, params=params) as resp:
        raw_resp = await resp.json()
        return models.RoshChodesh(**raw_resp)


async def get_generic_yomtov(
        name: str,
        location: Location,
        cl_offset: int,
        havdala_opinion: str
) -> models.YomTov:
    url = ZMANIM_API_URL.format('yom_tov')
    params = {
        'lat': str(location[0]),
        'lng': str(location[1]),
        'yomtov_name': name,
        'cl': str(cl_offset),
        'havdala': havdala_opinion
    }

    async with bot.session.get(url, params=params) as resp:
        raw_resp = await resp.json()
        return models.YomTov(**raw_resp)


async def get_generic_fast(name: str, location: Location, havdala_opinion: str) -> models.Fast:
    url = ZMANIM_API_URL.format('fast')
    params = {
        'lat': str(location[0]),
        'lng': str(location[1]),
        'fast_name': name,
        'havdala': havdala_opinion
    }

    async with bot.session.get(url, params=params) as resp:
        raw_resp = await resp.json()
        return models.Fast(**raw_resp)


async def get_generic_holiday(name: str) -> models.Holiday:
    url = ZMANIM_API_URL.format('holiday')
    params = {'holiday_name': name}

    async with bot.session.get(url, params=params) as resp:
        raw_resp = await resp.json()
        return models.Holiday(**raw_resp)


async def get_israel_holidays() -> models.IsraelHolidays:
    url = ZMANIM_API_URL.format('holiday')
    result = []
    settings: Optional[SimpleSettings] = None

    for name in ['yom_hashoah', 'yom_hazikaron', 'yom_haatzmaut', 'yom_yerushalaim']:
        params = {'holiday_name': name}

        async with bot.session.get(url, params=params) as resp:
            raw_resp = await resp.json()
            result.append((name, date.fromisoformat(raw_resp['date'])))

            if not settings:
                settings = raw_resp['settings']

    return models.IsraelHolidays(settings=settings, holiday_list=result)
