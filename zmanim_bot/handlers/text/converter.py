from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from ...misc import dp
from ...handlers.redirects import redirect_to_main_menu
from ...texts import buttons, messages
from ... import keyboards


@dp.message_handler(text=buttons.mm_converter)
async def handle_converter_entry(msg: Message):
    kb = keyboards.get_
