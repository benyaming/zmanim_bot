from typing import Any, List, Optional, Tuple

from aiogram.types import User

from ._storage import *
from .models import Location
from .models import User as BotUser

__all__ = [
    'Location',
    'get_or_create_user',
    'get_or_set_zmanim',
    'get_or_set_cl',
    'get_or_set_lang',
    'get_or_set_havdala',
    'get_or_set_location',
    'set_location_name',
    'activate_location',
    'delete_location',
    'get_or_set_processor_type',
    'get_or_set_omer_flag',
]


async def get_or_create_user() -> BotUser:
    user = User.get_current()
    return await _get_or_create_user(user)


async def get_or_set_lang(lang: str = None) -> Optional[str]:
    user = User.get_current()
    return await get_lang(user) if not lang else await set_lang(user, lang)


async def get_or_set_location(location: Tuple[float, float] = None) -> Location:
    user = User.get_current()
    return await get_location(user) if not location else await set_location(user, location)


async def set_location_name(new_name: str, old_name: str) -> List[Location]:
    user = User.get_current()
    return await do_set_location_name(user, new_name=new_name, old_name=old_name)


async def activate_location(name: str) -> List[Location]:
    user = User.get_current()
    return await do_activate_location(user, name)


async def delete_location(name: str) -> List[Location]:
    user = User.get_current()
    return await do_delete_location(user, name)


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
        else await set_processor_type(user, processor_type)


async def get_or_set_omer_flag(
        omer_flag: Optional[bool] = None,
        zmanim: Optional[Any] = None  # todo circullar import problem, refactor needed
) -> Optional[bool]:
    user = User.get_current()
    if omer_flag:
        omer_time = zmanim and zmanim.tzeis_8_5_degrees.isoformat()
        return await set_omer_flag(user, omer_flag, omer_time)
    return await get_omer_flag(user)
