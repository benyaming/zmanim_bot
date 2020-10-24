from aiogram.types import Message

import zmanim_bot.keyboards.inline
from zmanim_bot import api
from zmanim_bot.handlers.redirects import redirect_to_request_language, \
    redirect_to_request_location
from zmanim_bot.misc import dp
from zmanim_bot.texts.single import buttons, messages
from zmanim_bot.tracking import track


@dp.message_handler(text=buttons.sm_candle)
@track('Candle lighting selection')
async def settings_menu_cl(msg: Message):
    current_cl = await api.get_or_set_cl()
    kb = zmanim_bot.keyboards.inline.get_cl_settings_keyboard(current_cl)
    await msg.reply(messages.settings_cl, reply_markup=kb)


@dp.message_handler(text=buttons.sm_havdala)
@track('Havdala selection')
async def settings_menu_havdala(msg: Message):
    current_havdala = await api.get_or_set_havdala()
    kb = zmanim_bot.keyboards.inline.get_havdala_settings_keyboard(current_havdala)
    await msg.reply(messages.settings_havdala, reply_markup=kb)


@dp.message_handler(text=buttons.sm_zmanim)
@track('Zmanim selection')
async def settings_menu_zmanim(msg: Message):
    current_zmanim = await api.get_or_set_zmanim()
    kb = zmanim_bot.keyboards.inline.get_zmanim_settings_keyboard(current_zmanim)
    await msg.reply(messages.settings_zmanim, reply_markup=kb)


@dp.message_handler(commands=['language'])
@dp.message_handler(text=buttons.sm_lang)
@track('Language command')
async def handle_language_request(msg: Message):
    await redirect_to_request_language()


@dp.message_handler(commands=['location'])
@dp.message_handler(text=buttons.sm_location)
@track('Location command')
async def handle_start(msg: Message):
    await redirect_to_request_location(with_back=True)
