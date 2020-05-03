from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from ...misc import dp
from ...texts import buttons, messages
from ... import keyboards
from ..forms import GregorianDateState, JewishDateState


@dp.message_handler(text=buttons.mm_converter)
async def handle_converter_entry(msg: Message):
    kb = keyboards.get_converter_menu()
    await msg.reply(messages.init_converter, reply_markup=kb)


@dp.message_handler(text=buttons.conv_greg_to_jew)
async def start_greg_to_jew_converter(msg: Message):
    await GregorianDateState().waiting_for_gregorian_date.set()
    kb = keyboards.get_cancel_keyboard()
    await msg.reply(messages.conv_greg_to_jew_date_request, reply_markup=kb)


@dp.message_handler(text=buttons.conv_jew_to_greg)
async def start_jew_to_greg_converter(msg: Message):
    await JewishDateState.waiting_for_jewish_date.set()
    kb = keyboards.get_cancel_keyboard()
    await msg.reply(messages.conv_jew_to_greg_date_request, reply_markup=kb)
