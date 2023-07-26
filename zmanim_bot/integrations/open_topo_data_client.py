import logging

from aiogram import Bot

from zmanim_bot.config import config

OPEN_TOPO_DATA_URL = 'https://api.opentopodata.org/v1/'

async def get_elevation(lat: float, lng: float) -> int:
    url = f'{OPEN_TOPO_DATA_URL}{config.OPEN_TOPO_DATA_DB}'
    params = {
        'locations': f'{lat},{lng}'
    }
    session = await Bot.get_current().get_session()
    resp = await session.get(url, params=params)
    data = await resp.json()

    try:
        elevation = int(data['results'][0]['elevation'])
    except Exception as e:
        logging.exception(e)
        elevation = 0

    return elevation
