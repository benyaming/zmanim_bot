import logging
import asyncio

from aiogram import Dispatcher, Bot, types
from .config import BOT_TOKEN


logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, loop, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
