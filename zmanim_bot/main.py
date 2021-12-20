import aiogram_metrics
import sentry_sdk
from aiogram.utils.executor import start_polling, start_webhook
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from zmanim_bot.config import config
from zmanim_bot.handlers import register_handlers
from zmanim_bot.middlewares import setup_middlewares
from zmanim_bot.misc import dp, logger
from zmanim_bot.utils import ensure_mongo_index

sentry_sdk.init(dsn=config.SENTRY_KEY, integrations=[AioHttpIntegration()])


async def on_start(_):
    setup_middlewares()
    register_handlers()

    await ensure_mongo_index()

    if config.METRICS_DSN:
        await aiogram_metrics.register(config.METRICS_DSN, config.METRICS_TABLE_NAME)

    logger.info('Starting zmanim_api bot...')


async def on_close(_):
    await aiogram_metrics.close()


if __name__ == '__main__':
    if config.IS_PROD:
        start_webhook(dp, config.WEBHOOK_PATH, on_startup=on_start)
    else:
        start_polling(dp, on_startup=on_start, skip_updates=True)
