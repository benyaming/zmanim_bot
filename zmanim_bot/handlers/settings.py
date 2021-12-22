from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageNotModified
from aiogram_metrics import track

from zmanim_bot.handlers.utils.redirects import (redirect_to_main_menu)
from zmanim_bot.helpers import (CALL_ANSWER_OK)
from zmanim_bot.misc import bot
from zmanim_bot.service import settings_service
from zmanim_bot.utils import chat_action


@chat_action('text')
@track('Candle lighting selection')
async def settings_menu_cl(msg: Message):
    resp, kb = await settings_service.get_current_cl()
    await msg.reply(resp, reply_markup=kb)


async def set_cl(call: CallbackQuery):
    await call.answer(CALL_ANSWER_OK)

    kb = await settings_service.set_cl(call.data)
    try:
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)
    except MessageNotModified:
        pass


@chat_action('text')
@track('Havdala selection')
async def settings_menu_havdala(msg: Message):
    resp, kb = await settings_service.get_current_havdala()
    await msg.reply(resp, reply_markup=kb)


async def set_havdala(call: CallbackQuery):
    await call.answer(CALL_ANSWER_OK)

    kb = await settings_service.set_havdala(call.data)

    try:
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)
    except MessageNotModified:
        pass


@track('Zmanim selection')
async def settings_menu_zmanim(msg: Message):
    resp, kb = await settings_service.get_current_zmanim()
    await msg.reply(resp, reply_markup=kb)


async def set_zmanim(call: CallbackQuery):
    await call.answer(CALL_ANSWER_OK)

    kb = await settings_service.set_zmanim(call.data)
    try:
        await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)
    except MessageNotModified:
        pass


@chat_action('text')
@track('Omer Settings')
async def handle_omer_settings(msg: Message):
    resp, kb = await settings_service.get_current_omer()
    await msg.reply(resp, reply_markup=kb)


async def set_omer(call: CallbackQuery):
    await call.answer(CALL_ANSWER_OK)

    kb = await settings_service.set_omer(call.data)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)


@chat_action('text')
@track('Language command')
async def handle_language_request(_: Message):
    from aiogram import types
    kb = types.InlineKeyboardMarkup()
    kb.row(types.InlineKeyboardButton('search place', switch_inline_query_current_chat='', ))
    await _.reply('test test test', reply_markup=kb)


@chat_action('text')
@track('Language selected')
async def set_language(msg: Message):
    await settings_service.set_language(msg.text)
    return await redirect_to_main_menu()


@chat_action('text')
@track('Init report')
async def help_menu_report(msg: Message):
    resp, kb = await settings_service.init_report()
    await msg.reply(resp, reply_markup=kb)
