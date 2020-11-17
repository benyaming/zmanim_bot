from typing import Tuple, Optional, List

from aiogram.types import User
from aiopg import Pool
from aiogram import Dispatcher, types

from ..config import LOCATION_NUMBER_LIMIT
from ..exceptions import NoLocationException, NoLanguageException, NonUniqueLocatioinException, \
    MaxLocationLimitException
from ..misc import db_engine
from .models import User, UserInfo, Location, ZmanimSettings

__all__ = [
    'get_or_create_user',
    'get_cl_offset',
    'get_zmanim',
    'get_havdala',
    'get_lang',
    'get_location',
    'set_zmanim',
    'set_cl',
    'set_havdala',
    'set_lang',
    'set_location',
    'get_processor_type',
    'set_processor_type'
]


def validate_location(location: Location, locations: List[Location]):
    if len(locations) >= LOCATION_NUMBER_LIMIT:
        raise MaxLocationLimitException

    for loc in locations:
        if loc.lat == location.lat and loc.lng == location.lng:
            raise NonUniqueLocatioinException


async def get_or_create_user(user_id: int, first_name: str = None, last_name: str = None, username: str = None) -> User:
    user = await db_engine.find_one(User, User.user_id == user_id)

    if not user:
        user = User(
            user_id=user_id,
            personal_info=UserInfo(
                first_name=first_name,
                last_name=last_name,
                username=username
            )
        )
        await db_engine.save(user)

    return user


async def get_lang(user_id: int) -> Optional[str]:
    user = await get_or_create_user(user_id)
    lang = user.language
    if not lang:
        raise NoLanguageException
    return lang


async def set_lang(user_id: int, lang: str):
    user = await get_or_create_user(user_id)
    user.language = lang
    await db_engine.save(user)


async def get_location(user_id: int) -> Tuple[float, float]:
    user = await get_or_create_user(user_id)
    location = list(filter(lambda loc: loc.is_active is True, user.location_list))
    if not location:
        raise NoLocationException

    return location[0].lat, location[0].lng


async def set_location(user_id: int, location: Tuple[float, float]):
    location_obj = Location(
        lat=location[0],
        lng=location[1],
        name='main_loc',
        is_active=True
    )

    user = await get_or_create_user(user_id)
    validate_location(location_obj, user.location_list)

    for i in range(len(user.location_list)):
        user.location_list[i].is_active = False

    user.location_list.append(location_obj)
    await db_engine.save(user)


async def get_cl_offset(user_id: int) -> int:
    user = await get_or_create_user(user_id)
    return user.cl_offset


async def set_cl(user_id: int, cl: int):
    user = await get_or_create_user(user_id)
    user.cl_offset = cl
    await db_engine.save(user)


async def get_havdala(user_id: int) -> str:
    user = await get_or_create_user(user_id)
    return user.havdala_opinion


async def set_havdala(user_id: int, havdala: str):
    user = await get_or_create_user(user_id)
    user.havdala_opinion = havdala
    await db_engine.save(user)


async def get_zmanim(user_id: int) -> dict:
    user = await get_or_create_user(user_id)
    return user.zmanim_settings.dict()


async def set_zmanim(user_id: int, zmanim: dict):
    zmanim_obj = ZmanimSettings(**zmanim)
    user = await get_or_create_user(user_id)
    user.zmanim_settings = zmanim_obj
    await db_engine.save(user)


async def get_processor_type(user_id: int) -> str:
    user = await get_or_create_user(user_id)
    return user.processor_type


async def set_processor_type(user_id: int, processor_type: str):
    user = await get_or_create_user(user_id)
    user.processor_type = processor_type
    await db_engine.save(user)
