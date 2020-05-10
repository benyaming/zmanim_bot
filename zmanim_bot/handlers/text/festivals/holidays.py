from aiogram.types import Message

from ....misc import dp
from ....texts import buttons
from .... import zmanim_api


@dp.message_handler(text=buttons.hom_chanukah)
async def handle_chanukah(msg: Message):
    resp = await zmanim_api.get_generic_holiday('chanukah')
    await msg.reply(f'<code>{resp.json(exclude_none=True, by_alias=True, indent=2)}</code>')


@dp.message_handler(text=buttons.hom_tu_bishvat)
async def handle_tu_bi_shvat(msg: Message):
    resp = await zmanim_api.get_generic_holiday('tu_bi_shvat')
    await msg.reply(f'<code>{resp.json(exclude_none=True, by_alias=True, indent=2)}</code>')


@dp.message_handler(text=buttons.hom_purim)
async def handle_purim(msg: Message):
    resp = await zmanim_api.get_generic_holiday('purim')
    await msg.reply(f'<code>{resp.json(exclude_none=True, by_alias=True, indent=2)}</code>')


@dp.message_handler(text=buttons.hom_israel)
async def handle_israel_holidays(msg: Message):
    resp = await zmanim_api.get_generic_holiday('israel_holidays')
    await msg.reply(f'<code>{resp.json(exclude_none=True, by_alias=True, indent=2)}</code>')


@dp.message_handler(text=buttons.hom_lag_baomer)
async def handle_lag_baomer(msg: Message):
    resp = await zmanim_api.get_generic_holiday('lag_baomer')
    await msg.reply(f'<code>{resp.json(exclude_none=True, by_alias=True, indent=2)}</code>')
