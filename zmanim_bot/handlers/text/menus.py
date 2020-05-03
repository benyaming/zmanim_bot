from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from ...misc import dp
from ...handlers.redirects import redirect_to_main_menu
from ...texts import buttons, messages
from ... import keyboards


@dp.message_handler(text=[buttons.mm_holidays, buttons.hom_main])
async def handle_holidays_menu(msg: Message):
    kb = keyboards.get_holidays_menu()
    await msg.reply(messages.select, reply_markup=kb)


@dp.message_handler(text=buttons.hom_more)
async def handle_nore_holidays_menu(msg: Message):
    kb = keyboards.get_more_holidays_menu()
    await msg.reply(messages.select, reply_markup=kb)


@dp.message_handler(text=buttons.mm_fasts)
async def handle_fasts_menu(msg: Message):
    kb = keyboards.get_fast_menu()
    await msg.reply(messages.select, reply_markup=kb)


@dp.message_handler(text=[buttons.back, buttons.cancel], state="*")
async def handle_back(msg: Message, state: FSMContext):
    await state.finish()
    await redirect_to_main_menu()


@dp.message_handler(text=buttons.mm_help)
async def handle_help_menu(msg: Message):
    kb = keyboards.get_help_menu()
    await msg.reply(messages.init_help, reply_markup=kb)


@dp.message_handler(text=buttons.mm_settings)
async def handle_settings_menu(msg: Message):
    kb = keyboards.get_settings_menu()
    await msg.reply(messages.init_settings, reply_markup=kb)
