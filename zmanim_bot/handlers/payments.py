from aiogram.types import CallbackQuery, PreCheckoutQuery, Message, InputFile
from aiogram_metrics import track

from zmanim_bot.helpers import CallbackPrefixes
from zmanim_bot.misc import bot
from zmanim_bot.service import payments_service
from zmanim_bot.texts.single import messages
from zmanim_bot.utils import chat_action


@chat_action('text')
@track('Init donate')
async def handle_donate(call: CallbackQuery):
    amount = int(call.data.split(CallbackPrefixes.donate)[1])
    await call.answer()
    await payments_service.init_donate(amount)


@track('Pre-checkout')
async def handle_pre_checkout(query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)


async def on_success_payment(msg: Message):
    await bot.send_photo(msg.from_user.id, InputFile('./res/on_sucess_donate.jpg'), caption=messages.donate_thanks)
