from pydantic import BaseModel, Field

from zmanim_bot.config import config
from zmanim_bot.misc import bot


class ReverseGeocodingApiResponse(BaseModel):
    latitude: float
    longitude: float
    lookup_source: str = Field(alias='lookupSource')
    plus_code: str = Field(alias='pluseCode')


async def get_location_name(lat: float, lng: float, locality: str) -> str:
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
            name = f'{city}, {locality}'[:30]
        elif city or locality:
            name = (city or locality)[:30]
        else:
            name = f'{lat:.3f}, {lng:.3f}'
        return name


