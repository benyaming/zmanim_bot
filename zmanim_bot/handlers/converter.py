from aiogram.types import Message

from zmanim_bot.misc import dp
from zmanim_bot.tracking import track
from zmanim_bot.utils import chat_action
from zmanim_bot.texts.single import buttons
from zmanim_bot.service import converter_service
from zmanim_bot.handlers.forms import ConverterGregorianDateState


@dp.message_handler(commands=['converter_api'])
@dp.message_handler(text=buttons.mm_converter)
@chat_action('text')
@track('Entry to converter_api')
async def handle_converter_entry(msg: Message):
    resp, kb = converter_service.get_converter_entry_menu()
    await msg.reply(resp, reply_markup=kb)


@dp.message_handler(text=buttons.conv_greg_to_jew)
@chat_action('text')
@track('Converter - gregorian -> jewish')
async def start_greg_to_jew_converter(msg: Message):
    await ConverterGregorianDateState().waiting_for_gregorian_date.set()
    resp, kb = await converter_service.init_greg_to_jew()
    await msg.reply(resp, reply_markup=kb)


@dp.message_handler(text=buttons.conv_jew_to_greg)
@chat_action('text')
@track('Converter - jewish -> gregorian')
async def start_jew_to_greg_converter(msg: Message):
    resp, kb = await converter_service.init_jew_to_greg()
    await msg.reply(resp, reply_markup=kb)
