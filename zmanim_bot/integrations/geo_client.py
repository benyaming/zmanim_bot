from hashlib import md5
from typing import List

from aiogram.types import InlineQueryResultLocation

from zmanim_bot.config import config
from zmanim_bot.misc import bot


async def get_location_name(lat: float, lng: float, locality: str, *, no_trim: bool = False) -> str:
    params = {
        'latitude': lat,
        'longitude': lng,
        'localityLanguage': locality
    }
    async with bot.session.get(config.GEO_API_URL, params=params) as resp:
        raw_resp: dict = await resp.json()
        city = raw_resp.get('city')
        locality = raw_resp.get('locality')

        if city and locality and city != locality:
            name = f'{city}, {locality}'
            if not no_trim:
                name = name[:30]

        elif city or locality:
            name = (city or locality)
            if not no_trim:
                name = name[:30]

        else:
            name = f'{lat:.3f}, {lng:.3f}'
        return name


async def find_places_by_query(query: str, language: str) -> List[InlineQueryResultLocation]:
    url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json?'
    params = {
        'access_token': config.MAPBOX_API_KEY,
        'language': language,
        'types': 'place,locality,neighborhood,address'  # ,poi
    }
    results = []

    async with bot.session.get(url, params=params) as resp:
        raw_resp: dict = await resp.json()

    for feature in raw_resp.get('features', []):
        lng, lat = feature.get('center', (None, None))
        title: str = feature.get('place_name')

        if not all((lat, lng, title)):
            continue

        place_id = md5(title.encode()).hexdigest()
        results.append(InlineQueryResultLocation(id=place_id, latitude=lat, longitude=lng, title=title))

    return results
