from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from zmanim_bot.helpers import CallbackPrefixes, FeatureType, ZmanimType
from zmanim_bot.service import notifications_service
from zmanim_bot.states import CreateNotificationState


async def handle_new_notifications_menu(msg: Message):
    resp = 'select notification type:'  # todo
    kb = ''


async def init_notification(call: CallbackQuery):
    feature_type = call.data.split(CallbackPrefixes.init_notification_setup)[1]
    resp, kb = notifications_service.process_init_notification(feature_type)
    await Bot.get_current().send_message(call.message.chat.id, resp, reply_markup=kb)
    await call.answer()


async def init_zmanim_notification(call: CallbackQuery, state: FSMContext):
    # todo hide zmanim buttons
    zman_type = call.data.split(CallbackPrefixes.select_notification_zmanim)[1]

    await CreateNotificationState.waiting_for_offset_state.set()
    await state.update_data(
        {
            'feature': FeatureType.zmanim,
            'zman_type': ZmanimType(zman_type).name  # todo get enum value!
        }
    )

    resp = 'add offset to notification (send 0 for no ofset)'  # todo translate; +/- hint
    await Bot.get_current().send_message(call.message.chat.id, resp)


async def set_offset(msg: Message, state: FSMContext):
    try:
        offset = notifications_service.process_offset(msg.text)
    except ValueError:
        return await Bot.get_current().send_message(msg.from_user.id, 'incorrect offset')  # todo translate

    await state.update_data({'offset': offset})

    resp = 'write a message you want to get'  # todo translate
    await msg.reply(resp)
    await CreateNotificationState.next()


async def set_message(msg: Message, state: FSMContext):
    await state.update_data({'message': msg.text})

    resp = 'write a name for your notification'  # todo translate
    await msg.reply(resp)
    await CreateNotificationState.next()


async def set_name(msg: Message, state: FSMContext):
    data = await state.get_data()
    data['name'] = msg.text

    await notifications_service.create_notification(data)

    resp = f'notification {msg.text} saved, manage it in ssetings'  # todo translate
    await msg.reply(resp)
    await state.finish()


# todo fix state-based routing
