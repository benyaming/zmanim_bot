from ..misc import bot
from ..api import Location
from . import models
from ..config import ZMANIM_API_URL


__all__ = [
    'get_zmanim',
    'get_shabbat',
    'get_daf_yomi',
    'get_rosh_chodesh',
    'get_generic_yomtov',
    'get_generic_holiday',
    'get_generic_fast'
]


async def get_zmanim(location: Location, zmanim_settings: dict, date: str = None) -> models.Zmanim:
    url = ZMANIM_API_URL.format('zmanim')
    params = {
        'lat': str(location[0]),
        'lng': str(location[1]),
    }
    if date:
        params['date'] = date

    async with bot.session.post(url, params=params, json=zmanim_settings) as resp:
        raw_resp = await resp.json()
        return models.Zmanim(**raw_resp)


async def get_shabbat(location: Location, cl_offset: int, havdala_opinion: str,
                      date: str = None) -> models.Shabbat:
    url = ZMANIM_API_URL.format('shabbat')
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
        return models.Shabbat(**raw_resp)


async def get_daf_yomi(date=None) -> models.DafYomi:
    url = ZMANIM_API_URL.format('daf_yomi')
    params = None if not date else {'date': date}

    async with bot.session.get(url, params=params) as resp:
        raw_resp = await resp.json()
        return models.DafYomi(**raw_resp)


async def get_rosh_chodesh(date=None) -> models.RoshChodesh:
    url = ZMANIM_API_URL.format('rosh_chodesh')
    params = None if not date else {'date': date}

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
        'havdala': havdala_opinion,
        'date': '2020-01-01'
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

