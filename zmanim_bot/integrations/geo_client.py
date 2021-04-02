from pydantic import BaseModel, Field

from zmanim_bot.config import GEO_API_URL
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
    async with bot.session.get(GEO_API_URL, params=params) as resp:
        raw_resp: dict = await resp.json()
        return raw_resp.get('locality', f'{lat}, {lng}')


