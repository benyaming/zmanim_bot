import betterlogging as bl
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from motor.core import AgnosticCollection
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from .config import config

bl.basic_colorized_config(level=bl.INFO)
logger = bl.getLogger('zmanim_bot')

storage = RedisStorage2(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)
bot = Bot(config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
loop = bot.loop


motor_client = AsyncIOMotorClient(config.DB_URL)
collection: AgnosticCollection = motor_client[config.DB_NAME][config.DB_COLLECTION_NAME]
db_engine = AIOEngine(motor_client, database=config.DB_NAME)

