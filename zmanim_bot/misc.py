import asyncio

import betterlogging as bl
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from motor.core import AgnosticCollection
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from .config import (BOT_TOKEN, DB_COLLECTION_NAME, DB_NAME, DB_URL, REDIS_DB,
                     REDIS_HOST, REDIS_PORT)

bl.basic_colorized_config(level=bl.INFO)
logger = bl.getLogger('zmanim_bot')

loop = asyncio.get_event_loop()
storage = RedisStorage2(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
bot = Bot(BOT_TOKEN, loop, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

motor_client = AsyncIOMotorClient(DB_URL)
collection: AgnosticCollection = motor_client[DB_NAME][DB_COLLECTION_NAME]
db_engine = AIOEngine(motor_client, database=DB_NAME)

