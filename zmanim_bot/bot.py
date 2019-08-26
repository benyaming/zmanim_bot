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


@dp.message_handler(commands=['start'], state='*')
async def handle_start(msg: types.Message):
    response = 'start'
    await User.Menus.set()
    await bot.send_message(msg.chat.id, response)


@dp.message_handler(commands=['help'], state='*')
async def handle_start(msg: types.Message):
    th = await TextHandler.create(msg.chat.id, 'Help')
    #  TODO call __init__ synchronously
    await th.process_text()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=User.Menus)
async def handle_start(msg: types.Message,  state: FSMContext):
    print('ololo')

    th = await TextHandler.create(msg.chat.id, msg.text)
    #  TODO call __init__ synchronously
    await th.process_text()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=User.GregToHeb)
async def handle_start(msg: types.Message):
    th = await TextHandler.create(msg.chat.id, msg.text)
    #  TODO call __init__ synchronously
    await th.process_text()


# TODO proper folter
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(lambda message: message.text in ["cancel", "отмена"], state='*')
async def cancel_handler(msg: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    print ('hah')
    current_state = await state.get_state()
    print(current_state)
    logging.info('Cancelling state %r')
    # Cancel state and inform user about it
    await User.Menus.set()
    # And remove keyboard (just in case)
    th = await TextHandler.create(msg.chat.id, "Отмена")
    #  TODO call __init__ synchronously
    await th.process_text()






# todo handlers

if __name__ == '__main__':

    print (env['BOT_TOKEN'])
    start_polling(dp)
