import posthog
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from zmanim_bot.misc import dp
from zmanim_bot.utils import chat_action
from zmanim_bot.texts.single import buttons
from zmanim_bot.handlers.utils.redirects import redirect_to_main_menu


@dp.message_handler(commands=['start'])
@chat_action('text')
async def handle_start(msg: Message, state: FSMContext):
    await state.finish()
    await redirect_to_main_menu()
    posthog.identify(msg.from_user.id, message_id=msg.message_id)


@dp.message_handler(text=[buttons.back, buttons.cancel], state="*")
@chat_action('text')
async def handle_back(msg: Message, state: FSMContext):
    await state.finish()
    await redirect_to_main_menu()
