from aiogram.types import Message, CallbackQuery, ContentType

from zmanim_bot.config import LANGUAGE_LIST
from zmanim_bot.handlers.utils.redirects import redirect_to_request_language, \
    redirect_to_request_location, redirect_to_main_menu
from zmanim_bot.helpers import CallbackPrefixes, CALL_ANSWER_OK, LOCATION_PATTERN, \
    parse_coordinates
from zmanim_bot.misc import dp, bot
from zmanim_bot.tracking import track
from zmanim_bot.utils import chat_action
from zmanim_bot.texts.single import buttons
from zmanim_bot.service import settings_service


@dp.message_handler(text=buttons.sm_candle)
@chat_action('text')
@track('Candle lighting selection')
async def settings_menu_cl(msg: Message):
    resp, kb = await settings_service.get_current_cl()
    await msg.reply(resp, reply_markup=kb)


@dp.callback_query_handler(text_startswith=CallbackPrefixes.cl)
async def set_cl(call: CallbackQuery):
    await call.answer(CALL_ANSWER_OK)

    kb = await settings_service.set_cl(call.data)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)


@dp.message_handler(text=buttons.sm_havdala)
@chat_action('text')
@track('Havdala selection')
async def settings_menu_havdala(msg: Message):
    resp, kb = await settings_service.get_current_havdala()
    await msg.reply(resp, reply_markup=kb)


@dp.callback_query_handler(text_startswith=CallbackPrefixes.havdala)
async def set_havdala(call: CallbackQuery):
    await call.answer(CALL_ANSWER_OK)

    kb = await settings_service.set_havdala(call.data)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)


@dp.message_handler(text=buttons.sm_zmanim)
@track('Zmanim selection')
async def settings_menu_zmanim(msg: Message):
    resp, kb = await settings_service.get_current_zmanim()
    await msg.reply(resp, reply_markup=kb)


@dp.callback_query_handler(text_startswith=CallbackPrefixes.zmanim)
async def set_zmanim(call: CallbackQuery):
    await call.answer(CALL_ANSWER_OK)

    kb = await settings_service.set_zmanim(call.data)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)


@dp.message_handler(text=buttons.sm_omer)
@chat_action('omer')
@track('Omer Settings')
async def handle_omer_settings(msg: Message):
    resp, kb = await settings_service.get_current_havdala()
    await msg.reply(resp, reply_markup=kb)


@dp.callback_query_handler(text_startswith=CallbackPrefixes.omer)
async def set_omer(call: CallbackQuery):
    await call.answer(CALL_ANSWER_OK)

    kb = await settings_service.set_omer(call.data)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=kb)


@dp.message_handler(commands=['language'])
@dp.message_handler(text=buttons.sm_lang)
@chat_action('text')
@track('Language command')
async def handle_language_request(msg: Message):
    await redirect_to_request_language()


@dp.message_handler(text=LANGUAGE_LIST)
@chat_action('text')
@track('Language selected', attach_message_text=True)
async def set_language(msg: Message):
    await settings_service.set_language(msg.text)
    return await redirect_to_main_menu()


@dp.message_handler(commands=['location'])
@dp.message_handler(text=buttons.sm_location)
@chat_action('text')
@track('Location command')
async def location_request(msg: Message):
    await redirect_to_request_location(with_back=True)


@dp.message_handler(regexp=LOCATION_PATTERN)
@chat_action('text')
@track('Location regexp')
@dp.message_handler(content_types=[ContentType.LOCATION, ContentType.VENUE])
async def handle_location(msg: Message):
    if msg.location:
        lat = msg.location.latitude
        lng = msg.location.longitude
    else:
        lat, lng = parse_coordinates(msg.text)

    await settings_service.set_location(lat, lng)
    return await redirect_to_main_menu()


@dp.message_handler(commands=['report'])
@dp.message_handler(text=buttons.hm_report)
@chat_action('text')
@track('Init report')
async def help_menu_report(msg: Message):
    resp, kb = await settings_service.init_report()
    await msg.reply(resp, reply_markup=kb)
