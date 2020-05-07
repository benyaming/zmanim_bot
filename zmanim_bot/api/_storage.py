from typing import Tuple, Optional, List
from json import dumps

from aiopg import Pool
from aiogram import Dispatcher

from ..exceptions import NoLanguageException, NoLocationException


__all__ = [
    'track_user_',
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


async def track_user_(user_id: int, first_name: str, last_name: Optional[str], username: Optional[str]):
    query = 'INSERT INTO public.users VALUES (%s, %s, %s, %s) ' \
            'ON CONFLICT (user_id) DO UPDATE ' \
            'SET user_id = excluded.user_id,' \
            '    first_name = excluded.first_name,'\
            '    last_name = excluded.last_name,'\
            '    username = excluded.username;'
    args = (user_id, first_name, last_name, username)
    await _execute_query(query, args)


async def get_lang(user_id: int) -> str:
    query = 'SELECT lang FROM public.lang WHERE user_id = %s'

    lang = await _execute_query(query, (user_id,), return_result=True)
    if len(lang) == 0:
        raise NoLanguageException
    return lang[0][0]


async def set_lang(user_id: int, lang: str):
    query = 'INSERT INTO public.lang ' \
            'VALUES (%s, %s) ' \
            'ON CONFLICT (user_id) DO UPDATE ' \
            '  SET user_id = excluded.user_id, ' \
            '      lang = excluded.lang;'
    args = (user_id, lang)
    await _execute_query(query, args)


async def get_location(user_id: int) -> Tuple[float, float]:
    query = 'SELECT latitude, longitude from public.locations WHERE user_id = %s'
    location = await _execute_query(query, (user_id,), return_result=True)

    if len(location) == 0:
        raise NoLocationException
    return location[0][0], location[0][1]


async def set_location(user_id: int, location: Tuple[float, float]):
    query = 'INSERT INTO public.locations ' \
            'VALUES (%s, %s, %s) ' \
            'ON CONFLICT (user_id) DO UPDATE ' \
            '  SET user_id = excluded.user_id, ' \
            '      latitude = excluded.latitude,' \
            '      longitude = excluded.longitude;'
    args = (user_id, *location)
    await _execute_query(query, args)


async def get_cl_offset(user_id: int) -> int:
    query = 'SELECT cl_offset FROM zmanim_settings WHERE user_id = %s'
    cl = await _execute_query(query, (user_id,), return_result=True)

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
    cl = await _execute_query(query, (user_id,), return_result=True)

    return cl[0][0]


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
    return zmanim[0][0]


async def set_zmanim(user_id: int, zmanim: dict):
    query = 'INSERT INTO zmanim_settings (user_id, zmanim) ' \
            'VALUES (%s, %s) ' \
            'ON CONFLICT (user_id) DO UPDATE ' \
            '  SET user_id = excluded.user_id, ' \
            '      zmanim = excluded.zmanim;'
    args = (user_id, dumps(zmanim))
    await _execute_query(query, args)

