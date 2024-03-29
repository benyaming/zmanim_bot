from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ChatActions
from aiogram_metrics import track

from zmanim_bot.helpers import CallbackPrefixes
from zmanim_bot.keyboards.menus import get_cancel_keyboard
from zmanim_bot.repository.bot_repository import get_or_set_processor_type
from zmanim_bot.service import zmanim_service
from zmanim_bot.texts.single import messages
from zmanim_bot.utils import chat_action


@track('Zmanim')
async def handle_zmanim(_, state: FSMContext):
    chat_actions = {  # TODO refactor `@chat_action` to work with `@track`
        'image': ChatActions.upload_photo,
        'text': ChatActions.typing
    }
    processor_type = await get_or_set_processor_type()
    await chat_actions.get(processor_type, 'text')()

    await zmanim_service.send_zmanim(state=state)


@track('Zmanim geo-variant')
async def handle_update_zmanim(call: CallbackQuery):
    await call.answer()
    coordinates = call.data.split(CallbackPrefixes.update_zmanim)[1]

    if ':' in coordinates:
        coordinates, date = coordinates.split(':')
    else:
        date = None

    lat, lng = map(float, coordinates.split(','))
    await zmanim_service.update_zmanim(lat, lng, date)


@chat_action()
async def handle_zmanim_by_date_callback(call: CallbackQuery, state: FSMContext):
    await zmanim_service.send_zmanim(call=call, state=state)
    await call.answer()


@chat_action()
@track('Zmanim by date')
async def handle_zmanim_by_date(msg: Message):
    await zmanim_service.init_zmanim_by_date()
    await msg.reply(messages.greg_date_request, reply_markup=get_cancel_keyboard())


@chat_action()
@track('Shabbat')
async def handle_shabbat(_):
    await zmanim_service.get_shabbat()


@track('Shabbat geo-variant')
async def handle_update_shabbat(call: CallbackQuery, state: FSMContext):
    coordinates = call.data.split(CallbackPrefixes.update_shabbat)[1]
    lat, lng = map(float, coordinates.split(','))
    await zmanim_service.update_shabbat(lat, lng, state)
    await call.answer()


@chat_action()
@track('Daf yomi')
async def handle_daf_yomi(_):
    await zmanim_service.get_daf_yomi()


@chat_action()
@track('Rosh chodesh')
async def handle_rosh_chodesh(_):
    await zmanim_service.get_rosh_chodesh()
