import posthog
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from ..misc import dp
from ..texts.single import buttons
from .redirects import redirect_to_main_menu


@dp.message_handler(text=[buttons.back, buttons.cancel], state="*")
async def handle_back(msg: Message, state: FSMContext):
    await state.finish()
    await redirect_to_main_menu()


@dp.message_handler(commands=['start'])
async def handle_start(msg: Message, state):
    await state.finish()
    await redirect_to_main_menu()
    posthog.identify(msg.from_user.id, message_id=msg.message_id)
