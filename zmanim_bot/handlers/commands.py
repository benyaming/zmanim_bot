from asyncio import create_task

from aiogram.types import Message

from ..misc import dp
from ..exceptions import NoLanguageException
from ..api import track_user, get_or_set_zmanim
from .redirects import redirect_to_main_menu, redirect_to_request_location
from ..texts import buttons


@dp.message_handler(commands=['start'])
async def handle_start(msg: Message):
    await redirect_to_main_menu()
    create_task(track_user())


@dp.message_handler(commands=['q'])
async def handle_start(msg: Message):
    from ..keyboards import get_zmanim_settings_keyboard
    z = await get_or_set_zmanim()
    kb = get_zmanim_settings_keyboard(z)
    await msg.reply('test', reply_markup=kb)


@dp.message_handler(commands=['lang'])
@dp.message_handler(text=buttons.sm_lang)
async def handle_start(msg: Message):
    raise NoLanguageException


@dp.message_handler(commands=['location'])
@dp.message_handler(text=buttons.sm_location)
async def handle_start(msg: Message):
    await redirect_to_request_location(with_back=True)


# @dp.message_handler(commands=['help'])
# async def handle_start(msg: types.Message):
#     response = 'help'
#     await bot.send_message(msg.chat.id, response)
