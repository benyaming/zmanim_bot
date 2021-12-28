from typing import List, Optional, Tuple

from aiogram import types

from zmanim_bot.config import config
from zmanim_bot.exceptions import (ActiveLocationException,
                                   MaxLocationLimitException,
                                   NoLanguageException, NoLocationException,
                                   NonUniqueLocationException,
                                   NonUniqueLocationNameException)
from zmanim_bot.integrations.geo_client import get_location_name
from zmanim_bot.misc import db_engine
from .models import Location, User, UserInfo, ZmanimSettings

__all__ = [
    '_get_or_create_user',
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
    'do_set_location_name',
    'do_activate_location',
    'do_delete_location',
    'get_processor_type',
    'set_processor_type',
    'get_omer_flag',
    'set_omer_flag',
]


MAX_LOCATION_NAME_SIZE = 29


def validate_location_coordinates(location: Location, locations: List[Location]):
    if len(locations) >= config.LOCATION_NUMBER_LIMIT:
        raise MaxLocationLimitException

    for loc in locations:
        if loc.lat == location.lat and loc.lng == location.lng:
            raise NonUniqueLocationException


def validate_location_name(new_name: str, locations: List[Location]):
    for loc in locations:
        if loc.name == new_name:
            raise NonUniqueLocationNameException


async def _get_or_create_user(tg_user: types.User) -> User:
    user = await db_engine.find_one(User, User.user_id == tg_user.id)

    if not user:
        user = User(
            user_id=tg_user.id,
            personal_info=UserInfo(
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                username=tg_user.username
            )
        )
        await db_engine.save(user)
    elif user.personal_info.first_name != tg_user.first_name or \
         user.personal_info.last_name != tg_user.last_name or \
         user.personal_info.username != tg_user.username:
        user.personal_info = UserInfo(
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                username=tg_user.username
            )
        await db_engine.save(user)

    return user


async def get_lang(tg_user: types.User) -> Optional[str]:
    user = await _get_or_create_user(tg_user)
    lang = user.language
    if not lang:
        raise NoLanguageException
    return lang


async def set_lang(tg_user: types.User, lang: str):
    user = await _get_or_create_user(tg_user)
    user.language = lang
    await db_engine.save(user)


async def get_location(tg_user: types.User) -> Tuple[float, float]:
    user = await _get_or_create_user(tg_user)
    location = list(filter(lambda loc: loc.is_active is True, user.location_list))
    if not location:
        raise NoLocationException

    return location[0].lat, location[0].lng


async def set_location(tg_user: types.User, location: Tuple[float, float]) -> Location:
    user = await _get_or_create_user(tg_user)
    location_name = await get_location_name(location[0], location[1], user.language)
    if len(location_name) > MAX_LOCATION_NAME_SIZE:
        location_name = f'{location_name[:MAX_LOCATION_NAME_SIZE]}...'

    location_obj = Location(
        lat=location[0],
        lng=location[1],
        name=location_name,
        is_active=True
    )
    validate_location_coordinates(location_obj, user.location_list)

    for i in range(len(user.location_list)):
        user.location_list[i].is_active = False

    user.location_list.append(location_obj)
    await db_engine.save(user)
    return location_obj


async def do_set_location_name(tg_user: types.User, new_name: str, old_name: str) -> List[Location]:
    user = await _get_or_create_user(tg_user)
    location = list(filter(lambda l: l.name == old_name, user.location_list))

    if len(location) == 0:
        raise ValueError('Unknown old location name!')
    validate_location_name(new_name, user.location_list)

    if len(new_name) > MAX_LOCATION_NAME_SIZE:
        new_name = f'{new_name[:MAX_LOCATION_NAME_SIZE]}...'

    location = location[0]
    location.name = new_name

    location_index = user.location_list.index(location)
    user.location_list[location_index] = location
    await db_engine.save(user)
    return user.location_list


async def do_activate_location(tg_user: types.User, name: str) -> List[Location]:
    user = await _get_or_create_user(tg_user)

    if len(user.location_list) == 1:
        return user.location_list

    for location in user.location_list:
        location.is_active = False

    location = list(filter(lambda l: l.name == name, user.location_list))
    if len(location) == 0:
        raise ValueError('Unknown location name!')

    index = user.location_list.index(location[0])
    user.location_list[index].is_active = True

    await db_engine.save(user)
    return user.location_list


async def do_delete_location(tg_user: types.User, name: str) -> List[Location]:
    user = await _get_or_create_user(tg_user)
    location = list(filter(lambda l: l.name == name, user.location_list))

    if len(location) == 0:
        raise ValueError('Unknown location name!')
    if location[0].is_active:
        raise ActiveLocationException()

    user.location_list.remove(location[0])
    await db_engine.save(user)
    return user.location_list


async def get_cl_offset(tg_user: types.User) -> int:
    user = await _get_or_create_user(tg_user)
    return user.cl_offset


async def set_cl(tg_user: types.User, cl: int):
    user = await _get_or_create_user(tg_user)
    user.cl_offset = cl
    await db_engine.save(user)


async def get_havdala(tg_user: types.User) -> str:
    user = await _get_or_create_user(tg_user)
    return user.havdala_opinion


async def set_havdala(tg_user: types.User, havdala: str):
    user = await _get_or_create_user(tg_user)
    user.havdala_opinion = havdala
    await db_engine.save(user)


async def get_zmanim(tg_user: types.User) -> dict:
    user = await _get_or_create_user(tg_user)
    return user.zmanim_settings.dict()


async def set_zmanim(tg_user: types.User, zmanim: dict):
    zmanim_obj = ZmanimSettings(**zmanim)
    user = await _get_or_create_user(tg_user)
    user.zmanim_settings = zmanim_obj
    await db_engine.save(user)


async def get_processor_type(tg_user: types.User) -> str:
    user = await _get_or_create_user(tg_user)
    return user.processor_type


async def set_processor_type(tg_user: types.User, processor_type: str):
    user = await _get_or_create_user(tg_user)
    user.processor_type = processor_type
    await db_engine.save(user)


async def get_omer_flag(tg_user: types.User) -> bool:
    user = await _get_or_create_user(tg_user)
    return user.omer.is_enabled


async def set_omer_flag(tg_user: types.User, omer_flag: bool, omer_time: Optional[str] = None):
    user = await _get_or_create_user(tg_user)

    user.omer.is_enabled = omer_flag
    user.omer.notification_time = omer_time

    await db_engine.save(user)
