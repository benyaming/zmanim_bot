from hashlib import md5
from typing import List

from aiogram.types import InlineQuery, InlineQueryResultLocation

from zmanim_bot.integrations.geo_client import get_location_name, find_places_by_query
from zmanim_bot.misc import bot
from zmanim_bot.repository.bot_repository import get_or_create_user
from zmanim_bot.repository.models import User


async def get_locations_by_location(lat: float, lng: float, user: User) -> List[InlineQueryResultLocation]:
    location_name = await get_location_name(lat, lng, user.language, no_trim=True)
    result_id = md5(f'{lat}, {lng}'.encode()).hexdigest()
    return [InlineQueryResultLocation(id=result_id, latitude=lat, longitude=lng, title=location_name)]


async def handle_inline_location_query(query: InlineQuery):
    user = await get_or_create_user()

    if len(query.query) < 3:
        if not query.location:
            return  # too short query to search
        results = await get_locations_by_location(query.location.latitude, query.location.longitude, user)
    else:
        results = await find_places_by_query(query.query, user.language)

    await bot.answer_inline_query(query.id, results)
