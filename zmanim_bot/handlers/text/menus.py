from aiogram.types import Message

import zmanim_bot.keyboards.menus
from ...misc import dp
from ...texts.single import buttons, messages
from ... import keyboards
from ...tracking import track


@dp.message_handler(text=[buttons.mm_holidays, buttons.hom_main])
@track('Holidays menu')
async def handle_holidays_menu(msg: Message):
    kb = zmanim_bot.keyboards.menus.get_holidays_menu()
    await msg.reply(messages.select, reply_markup=kb)


@dp.message_handler(text=buttons.hom_more)
@track('More holidays menu')
async def handle_nore_holidays_menu(msg: Message):
    kb = zmanim_bot.keyboards.menus.get_more_holidays_menu()
    await msg.reply(messages.select, reply_markup=kb)


@dp.message_handler(text=buttons.mm_fasts)
@track('Fasts menu')
async def handle_fasts_menu(msg: Message):
    kb = zmanim_bot.keyboards.menus.get_fast_menu()
    await msg.reply(messages.select, reply_markup=kb)


@dp.message_handler(text=buttons.mm_help)
@track('Help menu')
async def handle_help_menu(msg: Message):
    kb = zmanim_bot.keyboards.menus.get_help_menu()
    await msg.reply(messages.init_help, reply_markup=kb)


@dp.message_handler(text=buttons.mm_settings)
@track('Settings menu')
async def handle_settings_menu(msg: Message):
    kb = zmanim_bot.keyboards.menus.get_settings_menu()
    await msg.reply(messages.init_settings, reply_markup=kb)
