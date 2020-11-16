from typing import Tuple, Optional, List
from json import dumps

from aiopg import Pool
from aiogram import Dispatcher, types

from ..config import LOCATION_NUMBER_LIMIT
from ..exceptions import NoLocationException, NoLanguageException, NonUniqueLocatioinException, \
    MaxLocationLimitException
from ..misc import db_engine
from .models import User, UserInfo, Location


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


def _get_pool() -> Pool:
    return Dispatcher.get_current()['db_pool']


async def _execute_query(query: str, args: tuple, *, return_result: bool = False) -> Optional[List[Tuple]]:
    pool = _get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, args)

            if not return_result:
                return

            ret = []
            async for row in cur:
                ret.append(row)

            return ret


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


async def create_default_settings(user_id: int):
    query = 'INSERT INTO public.zmanim_settings (user_id) VALUES (%s)'
    await _execute_query(query, (user_id,))


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
    query = 'SELECT latitude, longitude from public.locations WHERE user_id = %s'
    location = await _execute_query(query, (user_id,), return_result=True)

    if len(location) == 0:
        raise NoLocationException
    return location[0][0], location[0][1]


def validate_location(location: Location, locations: List[Location]):
    if len(locations) >= LOCATION_NUMBER_LIMIT:
        raise MaxLocationLimitException

    for loc in locations:
        if loc.lat == location.lat and loc.lng == location.lng:
            raise NonUniqueLocatioinException


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
    query = 'SELECT cl_offset FROM zmanim_settings WHERE user_id = %s'
    cl = await _execute_query(query, (user_id,), return_result=True)

    if len(cl) == 0:
        await create_default_settings(user_id)
        return await get_cl_offset(user_id)

    return cl[0][0]


async def set_cl(user_id: int, cl: int):
    query = 'INSERT INTO zmanim_settings (user_id, cl_offset) ' \
            'VALUES (%s, %s) ' \
            'ON CONFLICT (user_id) DO UPDATE ' \
            '  SET user_id = excluded.user_id, ' \
            '      cl_offset = excluded.cl_offset;'
    args = (user_id, cl)
    await _execute_query(query, args)


async def get_havdala(user_id: int) -> str:
    query = 'SELECT havdala_opinion FROM zmanim_settings WHERE user_id = %s'
    havdala = await _execute_query(query, (user_id,), return_result=True)

    if len(havdala) == 0:
        await create_default_settings(user_id)
        return await get_havdala(user_id)

    return havdala[0][0]


async def set_havdala(user_id: int, havdala: str):
    query = 'INSERT INTO zmanim_settings (user_id, havdala_opinion) ' \
            'VALUES (%s, %s) ' \
            'ON CONFLICT (user_id) DO UPDATE ' \
            '  SET user_id = excluded.user_id, ' \
            '      havdala_opinion = excluded.havdala_opinion;'
    args = (user_id, havdala)
    await _execute_query(query, args)


async def get_zmanim(user_id: int) -> dict:
    query = 'SELECT zmanim FROM zmanim_settings WHERE user_id = %s'
    zmanim = await _execute_query(query, (user_id,), return_result=True)

    if len(zmanim) == 0:
        await create_default_settings(user_id)
        return await get_zmanim(user_id)

    return zmanim[0][0]


async def set_zmanim(user_id: int, zmanim: dict):
    query = 'INSERT INTO zmanim_settings (user_id, zmanim) ' \
            'VALUES (%s, %s) ' \
            'ON CONFLICT (user_id) DO UPDATE ' \
            '  SET user_id = excluded.user_id, ' \
            '      zmanim = excluded.zmanim;'
    args = (user_id, dumps(zmanim))
    await _execute_query(query, args)


async def get_processor_type(user_id: int) -> str:
    return 'image'


async def set_processor_type(user_id: int, processor_type: str):
    pass
