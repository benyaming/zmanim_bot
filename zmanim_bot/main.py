from aiogram import Dispatcher
from aiogram.utils.executor import start_polling, start_webhook

import zmanim_bot.handlers
from zmanim_bot.config import IS_PROD, WEBHOOK_PATH
from zmanim_bot.misc import dp, logger
from zmanim_bot.utils import ensure_mongo_index


def fix_imports():
    _ = zmanim_bot.handlers


async def on_start(dispatcher: Dispatcher):
    await ensure_mongo_index()
    logger.info('Starting zmanim_api bot...')


if __name__ == '__main__':
    if IS_PROD:
        start_webhook(dp, WEBHOOK_PATH, on_startup=on_start)
    else:
        start_polling(dp, on_startup=on_start, skip_updates=True)

