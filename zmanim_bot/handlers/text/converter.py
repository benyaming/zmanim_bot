from aiogram.types import Message

import zmanim_bot.keyboards.menus
from ...misc import dp
from ...tracking import track
from ...texts.single import buttons, messages
from ..forms import ConverterGregorianDateState, ConverterJewishDateState
from ...utils import chat_action


@dp.message_handler(commands=['converter_api'])
@dp.message_handler(text=buttons.mm_converter)
@chat_action('text')
@track('Entry to converter_api')
async def handle_converter_entry(msg: Message):
    kb = zmanim_bot.keyboards.menus.get_converter_menu()
    await msg.reply(messages.init_converter, reply_markup=kb)


@dp.message_handler(text=buttons.conv_greg_to_jew)
@chat_action('text')
@track('Converter - gregorian -> jewish')
async def start_greg_to_jew_converter(msg: Message):
    await ConverterGregorianDateState().waiting_for_gregorian_date.set()
    kb = zmanim_bot.keyboards.menus.get_cancel_keyboard()
    await msg.reply(messages.greg_date_request, reply_markup=kb)


@dp.message_handler(text=buttons.conv_jew_to_greg)
@chat_action('text')
@track('Converter - jewish -> gregorian')
async def start_jew_to_greg_converter(msg: Message):
    await ConverterJewishDateState.waiting_for_jewish_date.set()
    kb = zmanim_bot.keyboards.menus.get_cancel_keyboard()
    await msg.reply(messages.jew_date_request, reply_markup=kb)
