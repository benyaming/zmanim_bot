from aiogram.types import CallbackQuery

from ... import api, zmanim_api
from ...helpers import CallbackPrefixes
from ...misc import dp, bot
from ...processors.image.image_processor import ZmanimImage
from ...utils import chat_action


@dp.callback_query_handler(text_startswith=CallbackPrefixes.zmanim_by_date)
@chat_action()
async def handle_cl_call(call: CallbackQuery):
    date = call.data.split(CallbackPrefixes.zmanim_by_date)[1]
    await call.answer()

    location = await api.get_or_set_location()
    zmanim_settings = await api.get_or_set_zmanim()
    data = await zmanim_api.get_zmanim(location, zmanim_settings, date)

    pic = ZmanimImage(data).get_image()
    await bot.send_photo(call.from_user.id, pic, reply_to_message_id=call.message.message_id)
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)

