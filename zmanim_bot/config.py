from os import environ


I18N_DOMAIN = 'zmanim_bot'
BOT_TOKEN = environ.get('BOT_TOKEN')

LANGUAGE_LIST = ['English', 'Русский']
LANGUAGE_SHORTCUTS = {
    'English': 'en',
    'Русский': 'ru'
}


DSN = f'dbname={environ.get("DB_NAME")} ' \
      f'user={environ.get("DB_USER")} ' \
      f'password={environ.get("DB_PASSWORD")} ' \
      f'host={environ.get("DB_HOST")} ' \
      f'port={environ.get("DB_PORT")}'
