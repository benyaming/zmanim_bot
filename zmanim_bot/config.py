from os import getenv
from typing import List

I18N_DOMAIN = 'zmanim_bot'
BOT_TOKEN = getenv('BOT_TOKEN')
POSTHOG_API_KEY = getenv('POSTHOG_API_KEY')

IS_PROD = bool(getenv('IS_PROD', False))
WEBHOOK_PATH = getenv('WEBHOOK_PATH', '/zmanim_bot')

LANGUAGE_LIST = ['English', 'Русский', 'עברית']
LANGUAGE_SHORTCUTS = {
    'English': 'en',
    'Русский': 'ru',
    'עברית': 'he'
}

DB_URL = getenv('DB_URL')
DB_NAME = getenv('DB_NAME')
DB_COLLECTION_NAME = getenv('DB_COLLECTION_NAME')

REDIS_HOST = getenv('REDIS_HOST')
REDIS_PORT = int(getenv('REDIS_PORT'))
REDIS_DB = int(getenv('REDIS_DB'))

ZMANIM_API_URL: str = getenv('ZMANIM_API_URL')
GEO_API_URL: str = getenv('GEO_API_URL')

REPORT_ADMIN_LIST: List[int] = [int(i) for i in getenv('REPORT_ADMIN_LIST', '').split(', ')]

LOCATION_NUMBER_LIMIT: int = int(getenv('LOCATION_NUMBER_LIMIT', 5))
SENTRY_PUBLIC_KEY: str = getenv('SENTRY_PUBLIC_KEY')

METRICS_DSN = getenv('METRICS_DSN')
METRICS_TABLE_NAME = getenv('METRICS_TABLE_NAME')
IS_METRICS_ENABLED = bool(METRICS_DSN)
