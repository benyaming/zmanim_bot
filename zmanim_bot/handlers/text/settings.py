from aiogram.types import Message

from zmanim_bot import api
from zmanim_bot import keyboards
from zmanim_bot.misc import dp, bot
from zmanim_bot.texts import buttons, messages


@dp.message_handler(text=buttons.sm_candle)
async def settings_menu_cl(msg: Message):
    current_cl = await api.get_or_set_cl()
    kb = keyboards.get_cl_keyboard(current_cl)
    await msg.reply(messages.settings_cl, reply_markup=kb)


@dp.message_handler(text=buttons.sm_havdala)
async def settings_menu_havdala(msg: Message):
    current_havdala = await api.get_or_set_havdala()
    kb = keyboards.get_havdala_keyboard(current_havdala)
    await msg.reply(messages.settings_cl, reply_markup=kb)


@dp.message_handler(text=buttons.sm_zmanim)
async def settings_menu_zmanim(msg: Message):
    current_zmanim = await api.get_or_set_zmanim()
    kb = keyboards.get_zmanim_settings_keyboard(current_zmanim)
    await msg.reply(messages.settings_zmanim, reply_markup=kb)

