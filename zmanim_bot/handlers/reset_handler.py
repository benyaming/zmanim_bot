from aiogram.dispatcher import FSMContext

from zmanim_bot.handlers.utils.redirects import redirect_to_main_menu
from zmanim_bot.utils import chat_action


@chat_action('text')
async def handle_start(_, state: FSMContext):
    await state.finish()
    await redirect_to_main_menu()


@chat_action('text')
async def handle_back(_, state: FSMContext):
    await state.finish()
    await redirect_to_main_menu()
