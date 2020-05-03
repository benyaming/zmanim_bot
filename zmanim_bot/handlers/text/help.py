from aiogram.types import Message

from zmanim_bot.misc import dp, bot
from zmanim_bot.states import Feedback
from zmanim_bot.texts import buttons, messages


@dp.message_handler(text=buttons.hm_report)
async def help_menu_report(msg: Message):
    await Feedback.waiting_for_feedback_text.set()
    await msg.reply(messages.init_report)

