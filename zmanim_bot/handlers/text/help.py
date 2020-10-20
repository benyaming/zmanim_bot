from aiogram.types import Message

from zmanim_bot.keyboards.menus import get_cancel_keyboard
from zmanim_bot.misc import dp
from zmanim_bot.states import FeedbackState
from zmanim_bot.texts.single import buttons, messages
from zmanim_bot.tracking import track


@dp.message_handler(text=buttons.hm_report)
@track('Init report')
async def help_menu_report(msg: Message):
    await FeedbackState.waiting_for_feedback_text.set()
    await msg.reply(messages.init_report, reply_markup=get_cancel_keyboard())

