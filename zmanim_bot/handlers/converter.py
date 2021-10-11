from aiogram.types import Message
from aiogram_metrics import track

from zmanim_bot.service import converter_service
from zmanim_bot.states import ConverterGregorianDateState
from zmanim_bot.utils import chat_action


@chat_action('text')
@track('Entry to converter_api')
async def handle_converter_entry(msg: Message):
    resp, kb = converter_service.get_converter_entry_menu()
    await msg.reply(resp, reply_markup=kb)


@chat_action('text')
@track('Converter - gregorian -> jewish')
async def start_greg_to_jew_converter(msg: Message):
    await ConverterGregorianDateState().waiting_for_gregorian_date.set()
    resp, kb = await converter_service.init_greg_to_jew()
    await msg.reply(resp, reply_markup=kb)


@chat_action('text')
@track('Converter - jewish -> gregorian')
async def start_jew_to_greg_converter(msg: Message):
    resp, kb = await converter_service.init_jew_to_greg()
    await msg.reply(resp, reply_markup=kb)
