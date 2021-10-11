import aiogram_metrics
import sentry_sdk
from aiogram.utils.executor import start_polling, start_webhook
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from zmanim_bot.config import IS_PROD, WEBHOOK_PATH, SENTRY_PUBLIC_KEY, METRICS_DSN, METRICS_TABLE_NAME, \
    IS_METRICS_ENABLED
from zmanim_bot.handlers import register_handlers
from zmanim_bot.middlewares import setup_middlewares
from zmanim_bot.misc import dp, logger
from zmanim_bot.utils import ensure_mongo_index

sentry_sdk.init(dsn=SENTRY_PUBLIC_KEY, integrations=[AioHttpIntegration()])


async def on_start(_):
    setup_middlewares()
    register_handlers()

    await ensure_mongo_index()

    if IS_METRICS_ENABLED:
        await aiogram_metrics.register(METRICS_DSN, METRICS_TABLE_NAME)

    logger.info('Starting zmanim_api bot...')


async def on_close(_):
    await aiogram_metrics.close()


if __name__ == '__main__':
    if IS_PROD:
        start_webhook(dp, WEBHOOK_PATH, on_startup=on_start)
    else:
        start_polling(dp, on_startup=on_start, skip_updates=True)
