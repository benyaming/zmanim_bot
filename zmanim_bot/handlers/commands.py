from asyncio import create_task

import posthog
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from ..keyboards.menus import get_help_menu
from ..misc import dp
from ..api import track_user
from .redirects import redirect_to_main_menu, redirect_to_request_location, \
    redirect_to_request_language
from ..texts.single import buttons
from ..texts.single.messages import init_help
from ..tracking import track


@dp.message_handler(text=[buttons.back, buttons.cancel], state="*")
async def handle_back(msg: Message, state: FSMContext):
    await state.finish()
    await redirect_to_main_menu()


@dp.message_handler(commands=['lang'])
@track('Lang command')
@dp.message_handler(text=buttons.sm_lang)
async def handle_language_request(msg: Message):
    await redirect_to_request_language()


@dp.message_handler(commands=['location'])
@track('Location command')
@dp.message_handler(text=buttons.sm_location)
async def handle_start(msg: Message):
    await redirect_to_request_location(with_back=True)


@dp.message_handler(commands=['help'])
async def handle_start(msg: Message):
    kb = get_help_menu()
    await msg.reply(init_help, reply_markup=kb)


@dp.message_handler(commands=['start'])
async def handle_start(msg: Message, state):
    await state.finish()
    await redirect_to_main_menu()
    posthog.identify(msg.from_user.id, message_id=msg.message_id)
    create_task(track_user())
