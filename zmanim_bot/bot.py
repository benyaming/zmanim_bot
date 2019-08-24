import asyncio
import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling, set_webhook
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher.storage import FSMContext

from settings import BOT_TOKEN
from zmanim_bot.text_handler import TextHandler
from os import environ as env

from zmanim_bot.states import UserStates as User

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(env['BOT_TOKEN'], loop, parse_mode=types.ParseMode.MARKDOWN)

storage = RedisStorage2(host=env['redis_host'], port=env['redis_port'])
dp = Dispatcher(bot, storage=storage, loop=loop)


@dp.message_handler(commands=['start'])
async def handle_start(msg: types.Message):
    response = 'start'
    User.MainMenu.set()
    await bot.send_message(msg.chat.id, response)


@dp.message_handler(commands=['help'])
async def handle_start(msg: types.Message):
    response = 'help'
    await bot.send_message(msg.chat.id, response)


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=User.MainMenu)
async def handle_start(msg: types.Message, state: FSMContext):
    th = await TextHandler.create(msg.chat.id, msg.text)
    #  TODO call __init__ synchronously
    await th.process_text()


# todo handlers

if __name__ == '__main__':

    print (env['BOT_TOKEN'])
    #start_polling(dp)
