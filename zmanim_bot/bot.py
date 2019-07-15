import asyncio
import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling, set_webhook

from settings import BOT_TOKEN
from zmanim_bot.text_handler import TextHandler


logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, loop, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def handle_start(msg: types.Message):
    response = 'start'
    await bot.send_message(msg.chat.id, response)


@dp.message_handler(commands=['help'])
async def handle_start(msg: types.Message):
    response = 'help'
    await bot.send_message(msg.chat.id, response)


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_start(msg: types.Message):
    th = await TextHandler.create(msg.chat.id, msg.text)
    await th.process_text()


start_polling(dp)
