from aiogram.types import Message

from zmanim_bot.keyboards.menus import get_cancel_keyboard
from zmanim_bot.misc import dp
from zmanim_bot.texts.single import buttons, messages
from zmanim_bot.tracking import track
from zmanim_bot.utils import chat_action
from zmanim_bot.service import zmanim_service


@dp.message_handler(text=buttons.mm_zmanim)
@chat_action()
@track('Zmanim')
async def handle_zmanim(msg: Message):
    resp = await zmanim_service.get_zmanim()
    await msg.reply_photo(resp)


@dp.message_handler(text=buttons.mm_shabbat)
@chat_action()
@track('Shabbat')
async def handle_shabbat(msg: Message):
    resp, kb = await zmanim_service.get_shabbat()
    await msg.reply_photo(resp, reply_markup=kb)


@dp.message_handler(text=buttons.mm_daf_yomi)
@chat_action()
@track('Daf yomi')
async def handle_daf_yomi(msg: Message):
    resp = await zmanim_service.get_daf_yomi()
    await msg.reply_photo(resp)


@dp.message_handler(text=buttons.mm_rh)
@chat_action()
@track('Rosh chodesh')
async def handle_rosh_chodesh(msg: Message):
    resp = await zmanim_service.get_rosh_chodesh()
    await msg.reply_photo(resp)


@dp.message_handler(text=buttons.mm_zmanim_by_date)
@chat_action()
@track('Zmanim by date')
async def handle_zmanim_by_date(msg: Message):
    await zmanim_service.init_zmanim_by_date()
    await msg.reply(messages.greg_date_request, reply_markup=get_cancel_keyboard())


# todo: закончить сервисы
# todo: переводы для ошибок и евр меясцев
# todo: шаблоны переводов должны совпадать с переводами
# todo:
# todo:
