import aiogram_metrics
import sentry_sdk
from aiogram.utils.executor import set_webhook, start_polling
from aiohttp import web
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from zmanim_bot.config import config
from zmanim_bot.handlers import register_handlers
from zmanim_bot.middlewares import setup_middlewares
from zmanim_bot.miniapp.api import register_miniapp_api
from zmanim_bot.misc import dp, logger, bot
from zmanim_bot.texts.commands import commands
from zmanim_bot.utils import ensure_mongo_index

sentry_sdk.init(dsn=config.SENTRY_KEY, integrations=[AioHttpIntegration()])

# Normalized against a trailing slash: a reverse proxy that strips the public
# prefix leaves WEBHOOK_PATH as '/', and the naive f-string would register
# '//miniapp' — unreachable from outside, since nginx merges double slashes.
MINIAPP_API_PATH = f"{config.WEBHOOK_PATH.rstrip('/')}/miniapp"

# Keeps the polling-mode API server alive for the process lifetime.
_dev_api_runner: web.AppRunner | None = None


async def _start_dev_miniapp_api():
    """Serve the mini-app API in polling (dev) mode, which has no webhook server."""
    global _dev_api_runner
    app = web.Application()
    register_miniapp_api(app, MINIAPP_API_PATH)
    _dev_api_runner = web.AppRunner(app)
    await _dev_api_runner.setup()
    await web.TCPSite(_dev_api_runner, port=config.MINIAPP_DEV_API_PORT).start()
    logger.info('Mini-app API (dev) on http://localhost:%s%s', config.MINIAPP_DEV_API_PORT, MINIAPP_API_PATH)


async def on_start(_):
    setup_middlewares()
    register_handlers()

    await bot.set_my_commands(commands)

    await ensure_mongo_index()

    if config.METRICS_DSN:
        await aiogram_metrics.register(config.METRICS_DSN, config.METRICS_TABLE_NAME)

    if not config.IS_PROD and config.MINIAPP_URL:
        await _start_dev_miniapp_api()

    logger.info('Starting zmanim bot...')


async def on_close(_):
    await aiogram_metrics.close()


if __name__ == '__main__':
    if config.IS_PROD:
        # The mini-app API rides on the same aiohttp server as the webhook
        # (start_webhook can't take a prebuilt app, so set_webhook + run_app).
        app = web.Application()
        register_miniapp_api(app, MINIAPP_API_PATH)
        executor = set_webhook(dp, config.WEBHOOK_PATH, on_startup=on_start, web_app=app)
        executor.run_app()
    else:
        start_polling(dp, on_startup=on_start, skip_updates=True)
