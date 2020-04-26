from typing import Tuple

from aiopg import Pool
from aiogram import Dispatcher
from aiogram.types import User

from .exceptions import NoLanguageException, NoLocationException


def _get_pool() -> Pool:
    return Dispatcher.get_current()['db_pool']


async def track_user():
    user = User.get_current()
    query = 'INSERT INTO public.users VALUES (%s, %s, %s, %s) ' \
            'ON CONFLICT (user_id) DO UPDATE ' \
            'SET user_id = excluded.user_id,' \
            '    first_name = excluded.first_name,'\
            '    last_name = excluded.last_name,'\
            '    username = excluded.username;'

    pool = _get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, (user.id, user.first_name, user.last_name, user.username))


async def _save_lang(lang: str):
    user = User.get_current()
    query = 'INSERT INTO public.lang ' \
            'VALUES (%s, %s) ' \
            'ON CONFLICT (user_id) DO UPDATE ' \
            '  SET user_id = excluded.user_id, ' \
            '      lang = excluded.lang;'

    pool = _get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, (user.id, lang))


async def _get_lang() -> str:
    user = User.get_current()
    pool = _get_pool()
    query = 'SELECT lang FROM public.lang WHERE user_id = %s'

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, (user.id,))

            ret = []
            async for row in cur:
                ret.append(row)

            if len(ret) == 0:
                raise NoLanguageException
            return ret[0][0]


async def _save_location(location: Tuple[float, float]):
    user = User.get_current()
    lat, lng = location
    query = 'INSERT INTO public.locations ' \
            'VALUES (%s, %s, %s) ' \
            'ON CONFLICT (user_id) DO UPDATE ' \
            '  SET user_id = excluded.user_id, ' \
            '      latitude = excluded.latitude,' \
            '      longitude = excluded.longitude;'

    pool = _get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, (user.id, lat, lng))


async def _get_location() -> Tuple[float, float]:
    user = User.get_current()
    query = 'SELECT latitude, longitude from public.locations WHERE user_id = %s'

    pool = _get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, (user.id,))

            ret = []
            async for row in cur:
                ret.append(row)

            if len(ret) == 0:
                raise NoLocationException
            return float(ret[0][0]), float(ret[0][1])


async def get_or_set_lang(lang: str = None) -> str:
    return await _get_lang() if not lang else await _save_lang(lang)


async def get_or_set_location(location: Tuple[float, float]) -> Tuple[float, float]:
    return await _get_location() if not location else await _save_location(location)
