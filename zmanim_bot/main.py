import aiopg
from aiogram import Dispatcher
from aiogram.utils.executor import start_polling, start_webhook

import zmanim_bot.handlers
from zmanim_bot.config import DSN, IS_PROD, WEBHOOK_PATH
from zmanim_bot.misc import dp, logger


def fix_imports():
    _ = zmanim_bot.handlers


async def on_start(dispatcher: Dispatcher):
    db_conn = await aiopg.create_pool(DSN)
    dispatcher['db_pool'] = db_conn
    logger.info('Starting zmanim bot...')


if __name__ == '__main__':
    if IS_PROD:
        start_webhook(dp, WEBHOOK_PATH, on_startup=on_start)
    else:
        start_polling(dp, on_startup=on_start, skip_updates=True)

