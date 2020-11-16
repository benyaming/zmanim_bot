from os import getenv
from typing import List

I18N_DOMAIN = 'zmanim_bot'
BOT_TOKEN = getenv('BOT_TOKEN')
POSTHOG_API_KEY = getenv('POSTHOG_API_KEY')

IS_PROD = bool(getenv('IS_PROD', False))
WEBHOOK_PATH = getenv('WEBHOOK_PATH', '/zmanim_bot')

LANGUAGE_LIST = ['English', 'Русский']
LANGUAGE_SHORTCUTS = {
    'English': 'en',
    'Русский': 'ru'
}


DSN = f'dbname={getenv("DB_NAME")} ' \
      f'user={getenv("DB_USER")} ' \
      f'password={getenv("DB_PASSWORD")} ' \
      f'host={getenv("DB_HOST")} ' \
      f'port={getenv("DB_PORT")}'

DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
DB_NAME = getenv('DB_NAME')
DB_COLLECTION_NAME = getenv('DB_COLLECTION_NAME')

REDIS_HOST = getenv('REDIS_HOST')
REDIS_PORT = int(getenv('REDIS_PORT'))
REDIS_DB = int(getenv('REDIS_DB'))

ZMANIM_API_URL: str = getenv('ZMANIM_API_URL')

REPORT_ADMIN_LIST: List[int] = [int(i) for i in getenv('REPORT_ADMIN_LIST', '').split(', ')]

LOCATION_NUMBER_LIMIT: int = int(getenv('LOCATION_NUMBER_LIMIT', 5))
