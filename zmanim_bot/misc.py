import logging
import asyncio

from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from .config import BOT_TOKEN, REDIS_HOST, REDIS_PORT, REDIS_DB


logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()
storage = RedisStorage2(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
bot = Bot(BOT_TOKEN, loop, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
