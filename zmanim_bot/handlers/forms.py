from aiogram.types import Message

from ..misc import dp, bot
from ..states import GregorianDate, HebrewDate, Feedback


@dp.message_handler(state=Feedback.waiting_for_feedback_text)
async def handle_report(msg: Message):
    report_message = msg.text
    resp = f'REPORT:\n\n<i>{report_message}</i>'
    await Feedback.next()
    await bot.send_message(msg.from_user.id, resp)
