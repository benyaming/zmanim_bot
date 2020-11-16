from typing import Tuple, Optional

from aiogram.types import User

from ._storage import *

__all__ = [
    'Location',
    'track_user',
    'get_or_set_zmanim',
    'get_or_set_cl',
    'get_or_set_lang',
    'get_or_set_havdala',
    'get_or_set_location',
    'get_or_set_processor_type'
]


async def track_user():
    user = User.get_current()
    return await get_or_create_user(user.id, user.first_name, user.last_name, user.username)


async def get_or_set_lang(lang: str = None) -> Optional[str]:
    user = User.get_current()
    return await get_lang(user.id) if not lang else await set_lang(user.id, lang)


Location = Tuple[float, float]


async def get_or_set_location(location: Location = None) -> Optional[Location]:
    user = User.get_current()
    return await get_location(user.id) if not location else await set_location(user.id, location)


async def get_or_set_cl(cl: int = None) -> Optional[int]:
    user = User.get_current()
    return await get_cl_offset(user.id) if not cl else await set_cl(user.id, cl)


async def get_or_set_zmanim(zmanim: dict = None) -> Optional[dict]:
    user = User.get_current()
    return await get_zmanim(user.id) if not zmanim else await set_zmanim(user.id, zmanim)


async def get_or_set_havdala(havdala: str = None) -> Optional[str]:
    user = User.get_current()
    return await get_havdala(user.id) if not havdala else await set_havdala(user.id, havdala)


async def get_or_set_processor_type(processor_type: Optional[str] = None) -> Optional[str]:
    user = User.get_current()
    return await get_processor_type(user.id) if not processor_type \
        else set_processor_type(user.id, processor_type)
