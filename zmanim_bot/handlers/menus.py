from aiogram.types import Message
from aiogram_metrics import track

from zmanim_bot.keyboards import menus
from zmanim_bot.keyboards.inline import DONATE_KB
from zmanim_bot.texts.single import messages
from zmanim_bot.utils import chat_action


@chat_action('text')
@track('Holidays menu')
async def handle_holidays_menu(msg: Message):
    kb = menus.get_holidays_menu()
    await msg.reply(messages.select, reply_markup=kb)


@chat_action('text')
# @track('More holidays menu')
async def handle_more_holidays_menu(msg: Message):
    kb = menus.get_more_holidays_menu()
    await msg.reply(messages.select, reply_markup=kb)


@chat_action('text')
# @track('Fasts menu')
async def handle_fasts_menu(msg: Message):
    kb = menus.get_fast_menu()
    await msg.reply(messages.select, reply_markup=kb)


@chat_action('text')
# @track('Settings menu')
async def handle_settings_menu(msg: Message):
    kb = menus.get_settings_menu()
    await msg.reply(messages.init_settings, reply_markup=kb)


@chat_action('text')
@track('Donate button')
async def handle_donate(msg: Message):
    await msg.reply(messages.donate_init, reply_markup=DONATE_KB)
