from aiogram import Dispatcher
from aiogram.utils.executor import start_polling, start_webhook

import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
import zmanim_bot.handlers
from zmanim_bot.config import IS_PROD, WEBHOOK_PATH, SENTRY_PUBLIC_KEY, METRICS_DSN, METRICS_TABLE_NAME
from zmanim_bot.misc import dp, logger
from zmanim_bot.utils import ensure_mongo_index
from zmanim_bot.middlewares import sentry_context_middleware

import aiogram_metrics


sentry_sdk.init(
    dsn=SENTRY_PUBLIC_KEY,
    integrations=[AioHttpIntegration()]
)


def fix_imports():
    _ = zmanim_bot.handlers
    __ = sentry_context_middleware


async def on_start(dispatcher: Dispatcher):
    await ensure_mongo_index()
    await aiogram_metrics.register(METRICS_DSN, METRICS_TABLE_NAME)
    logger.info('Starting zmanim_api bot...')


async def on_close(dispatcher: Dispatcher):
    await aiogram_metrics.close()


if __name__ == '__main__':
    if IS_PROD:
        start_webhook(dp, WEBHOOK_PATH, on_startup=on_start)
    else:
        start_polling(dp, on_startup=on_start, skip_updates=True)
