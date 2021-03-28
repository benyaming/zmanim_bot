import betterlogging as bl
import asyncio

from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from motor.core import AgnosticCollection
from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient

from .config import BOT_TOKEN, REDIS_HOST, REDIS_PORT, REDIS_DB, DB_URL, DB_NAME, DB_COLLECTION_NAME

logger = bl.get_colorized_logger('zmanim_bot')
logger.setLevel(bl.INFO)

loop = asyncio.get_event_loop()
storage = RedisStorage2(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
bot = Bot(BOT_TOKEN, loop, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

motor_client = AsyncIOMotorClient(DB_URL)
collection: AgnosticCollection = motor_client[DB_NAME][DB_COLLECTION_NAME]
db_engine = AIOEngine(motor_client, database=DB_NAME)

