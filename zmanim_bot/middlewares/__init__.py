from zmanim_bot.misc import dp
from .black_list_middleware import BlackListMiddleware
from .i18n import i18n_
from .sentry_context_middleware import SentryContextMiddleware


def setup_middlewares():
    dp.middleware.setup(SentryContextMiddleware())
    dp.middleware.setup(i18n_)
    dp.middleware.setup(BlackListMiddleware())
