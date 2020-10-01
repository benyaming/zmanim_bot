from asyncio import create_task

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from ..misc import dp
from ..api import track_user
from .redirects import redirect_to_main_menu, redirect_to_request_location, \
    redirect_to_request_language
from ..texts.single import buttons


@dp.message_handler(text=[buttons.back, buttons.cancel], state="*")
async def handle_back(msg: Message, state: FSMContext):
    await state.finish()
    await redirect_to_main_menu()


@dp.message_handler(commands=['lang'])
@dp.message_handler(text=buttons.sm_lang)
async def handle_language_request(msg: Message):
    await redirect_to_request_language()


@dp.message_handler(commands=['location'])
@dp.message_handler(text=buttons.sm_location)
async def handle_start(msg: Message):
    await redirect_to_request_location(with_back=True)


# @dp.message_handler(commands=['help'])
# async def handle_start(msg: Message):
#     response = 'help'
#     await bot.send_message(msg.chat.id, response)


@dp.message_handler(commands=['start'], state='*')
async def handle_start(msg: Message, state: FSMContext):
    await state.finish()
    await redirect_to_main_menu()
    create_task(track_user())
