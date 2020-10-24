from asyncio import create_task

from aiogram.types import Message, ContentType
from aiogram.dispatcher import FSMContext

from ..misc import dp, bot
from ..states import (
    ConverterGregorianDateState,
    ConverterJewishDateState,
    FeedbackState,
    ZmanimGregorianDateState
)
from .. import converter
from ..helpers import parse_date
from .redirects import redirect_to_main_menu
from .. import api
from ..zmanim_api import get_zmanim
from ..processors.image.image_processor import ZmanimImage
from ..texts.single import messages, buttons
from ..keyboards.menus import get_report_keyboard
from ..admin.report_management import send_report_to_admins


# REPORTS


@dp.message_handler(state=FeedbackState.waiting_for_feedback_text)
async def handle_report(msg: Message, state: FSMContext):
    report = {
        'message': msg.text,
        'message_id': msg.message_id,
        'user_id': msg.from_user.id,
        'media_ids': []
    }
    await state.set_data(report)
    await FeedbackState.next()

    kb = get_report_keyboard()
    await bot.send_message(msg.chat.id, messages.reports_text_received, reply_markup=kb)


@dp.message_handler(text=buttons.done, state=FeedbackState.waiting_for_payload)
async def handle_done_report(msg: Message, state: FSMContext):
    report = await state.get_data()
    await state.finish()
    await redirect_to_main_menu(messages.reports_created)
    create_task(send_report_to_admins(report))


@dp.message_handler(content_types=ContentType.ANY, state=FeedbackState.waiting_for_payload)
async def handle_report_payload(msg: Message, state: FSMContext):
    if msg.content_type != ContentType.PHOTO:
        return await msg.reply(messages.reports_incorrect_media_type)

    report = await state.get_data()
    report['media_ids'].append((msg.photo[-1].file_id, 'photo'))
    await state.set_data(report)

    await msg.reply(messages.reports_media_received)


# CONVERTER #

@dp.message_handler(state=ConverterGregorianDateState.waiting_for_gregorian_date)
async def handle_converter_gregorian_date(msg: Message, state: FSMContext):
    resp, kb = converter.convert_greg_to_heb(msg.text)
    await state.finish()
    await msg.reply(resp, reply_markup=kb)
    await redirect_to_main_menu()


@dp.message_handler(state=ConverterJewishDateState.waiting_for_jewish_date)
async def handle_converter_jewish_date(msg: Message, state: FSMContext):
    resp, kb = converter.convert_heb_to_greg(msg.text)
    await state.finish()
    await msg.reply(resp, reply_markup=kb)
    await redirect_to_main_menu()


# ZMANIM #

@dp.message_handler(state=ZmanimGregorianDateState.waiting_for_gregorian_date)
async def handle_zmanim_gregorian_date(msg: Message, state: FSMContext):
    date = parse_date(msg.text)
    location = await api.get_or_set_location()
    zmanim_settings = await api.get_or_set_zmanim()

    data = await get_zmanim(location, zmanim_settings, date)
    pic = ZmanimImage(data).get_image()
    await msg.reply_photo(pic)
    await state.finish()
    await redirect_to_main_menu()
