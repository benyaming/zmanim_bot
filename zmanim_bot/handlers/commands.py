from asyncio import create_task

from aiogram.types import Message

from zmanim_bot.misc import bot, dp
from ..exceptions import NoLocationException, NoLanguageException, IncorrectTextException
from ..storage import track_user
from .redirects import redirect_to_main_menu
from ..texts import buttons


@dp.message_handler(commands=['start'])
async def handle_start(msg: Message):
    await redirect_to_main_menu()
    create_task(track_user())


@dp.message_handler(commands=['q'])
async def handle_start(msg: Message):
    raise IncorrectTextException()
    # await bot.send_message(msg.chat.id, response)


# @dp.message_handler(commands=['help'])
# async def handle_start(msg: types.Message):
#     response = 'help'
#     await bot.send_message(msg.chat.id, response)
