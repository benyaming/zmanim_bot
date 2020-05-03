from os import getenv


I18N_DOMAIN = 'zmanim_bot'
BOT_TOKEN = getenv('BOT_TOKEN')

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

REDIS_HOST = getenv('REDIS_HOST')
REDIS_PORT = int(getenv('REDIS_PORT'))
REDIS_DB = int(getenv('REDIS_DB'))
