import aiopg
from aiogram import Dispatcher
from aiogram.utils.executor import start_polling

import zmanim_bot.handlers
from zmanim_bot.config import DSN
from zmanim_bot.misc import dp


def fix_imports():
    _ = zmanim_bot.handlers


async def on_start(dispatcher: Dispatcher):
    db_conn = await aiopg.create_pool(DSN)
    dispatcher['db_pool'] = db_conn


start_polling(dp, on_startup=on_start, skip_updates=True)
# from zmanim_bot.processors.image.image_processor import test
# test()


# ---------------
# TODO date converter - jewish month and both weekdays not converts to string

