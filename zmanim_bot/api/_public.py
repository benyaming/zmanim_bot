from typing import Tuple, Optional

from aiogram.types import User

from .storage import (
    _track_user,
    get_lang,
    set_lang,
    get_location,
    set_location,
    get_cl,
    set_cl,
    get_zmanim,
    set_zmanim
)


async def track_user():
    user = User.get_current()
    return await _track_user(user.id, user.first_name, user.last_name, user.username)


async def get_or_set_lang(lang: str = None) -> Optional[str]:
    user = User.get_current()
    return await get_lang(user.id) if not lang else await set_lang(user.id, lang)


async def get_or_set_location(location: Tuple[float, float]) -> Optional[Tuple[float, float]]:
    user = User.get_current()
    return await get_location(user.id) if not location else await set_location(user.id, location)


async def get_or_set_cl(cl: int = None) -> Optional[int]:
    user = User.get_current()
    return await get_cl(user.id) if not cl else await set_cl(user.id, cl)


async def get_or_set_zmanim(zmanim: dict = None) -> Optional[dict]:
    user = User.get_current()
    return await get_zmanim(user.id) if not zmanim else await set_zmanim(user.id, zmanim)

