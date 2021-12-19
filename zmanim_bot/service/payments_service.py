from datetime import datetime as dt

from aiogram.types import LabeledPrice, User

from zmanim_bot.config import PAYMENTS_PROVIDER_TOKEN
from zmanim_bot.misc import bot
from zmanim_bot.texts.single import messages


async def init_donate(amount: int):
    user = User.get_current()
    invoice_title = messages.donate_invoice_title.value.format(amount)
    price = int(amount) * 100

    await bot.send_invoice(
        user.id,
        title=invoice_title,
        description=messages.donate_invoice_description.value.format(amount),
        payload=f'donate:{amount}:usd:{user.id}:{dt.now().isoformat()}',
        provider_token=PAYMENTS_PROVIDER_TOKEN,
        currency='usd',
        prices=[LabeledPrice(invoice_title, price)],
        provider_data=['qweqweqwe']
    )
