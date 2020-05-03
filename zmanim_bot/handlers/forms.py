from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from ..misc import dp, bot
from ..states import GregorianDateState, JewishDateState, FeedbackState
from .. import converter
from .redirects import redirect_to_main_menu


@dp.message_handler(state=FeedbackState.waiting_for_feedback_text)
async def handle_report(msg: Message):
    report_message = msg.text
    resp = f'REPORT:\n\n<i>{report_message}</i>'
    await FeedbackState.next()
    await bot.send_message(msg.from_user.id, resp)


@dp.message_handler(state=GregorianDateState.waiting_for_gregorian_date)
async def handle_converter_gregorian_date(msg: Message, state: FSMContext):
    resp = converter.convert_greg_to_heb(msg.text)
    await msg.reply(resp)
    await state.finish()
    await redirect_to_main_menu()


@dp.message_handler(state=JewishDateState.waiting_for_jewish_date)
async def handle_converter_jewish_date(msg: Message, state: FSMContext):
    resp = converter.convert_heb_to_greg(msg.text)
    await msg.reply(resp)
    await state.finish()
    await redirect_to_main_menu()

