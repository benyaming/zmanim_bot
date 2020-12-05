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
    return await get_or_create_user(user)


async def get_or_set_lang(lang: str = None) -> Optional[str]:
    user = User.get_current()
    return await get_lang(user) if not lang else await set_lang(user, lang)


Location = Tuple[float, float]


async def get_or_set_location(location: Location = None) -> Optional[Location]:
    user = User.get_current()
    return await get_location(user) if not location else await set_location(user, location)


async def get_or_set_cl(cl: int = None) -> Optional[int]:
    user = User.get_current()
    return await get_cl_offset(user) if not cl else await set_cl(user, cl)


async def get_or_set_zmanim(zmanim: dict = None) -> Optional[dict]:
    user = User.get_current()
    return await get_zmanim(user) if not zmanim else await set_zmanim(user, zmanim)


async def get_or_set_havdala(havdala: str = None) -> Optional[str]:
    user = User.get_current()
    return await get_havdala(user) if not havdala else await set_havdala(user, havdala)


async def get_or_set_processor_type(processor_type: Optional[str] = None) -> Optional[str]:
    user = User.get_current()
    return await get_processor_type(user) if not processor_type \
        else set_processor_type(user, processor_type)
