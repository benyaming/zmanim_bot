from typing import List, Dict, Optional

from pydantic import BaseSettings, Field, validator


class Config(BaseSettings):

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    I18N_DOMAIN: str = Field('zmanim_bot')
    BOT_TOKEN: str = Field(env='BOT_TOKEN')

    IS_PROD: bool = Field(False, env='IS_PROD')
    WEBHOOK_PATH: str = Field('/zmanim_bot', env='WEBHOOK_PATH')

    LANGUAGE_LIST: List[str] = Field(['English', 'Русский', 'עברית'])
    LANGUAGE_SHORTCUTS: Dict[str, str] = Field({
        'English': 'en',
        'Русский': 'ru',
        'עברית': 'he'
    })

    DB_URL: str = Field('localhost', env='DB_URL')
    DB_NAME: str = Field(env='DB_NAME')
    DB_COLLECTION_NAME: str = Field(env='DB_COLLECTION_NAME')

    REDIS_HOST: str = Field(env='REDIS_HOST')
    REDIS_PORT: int = Field(env='REDIS_PORT')
    REDIS_DB: int = Field(env='REDIS_DB')

    ZMANIM_API_URL: str = Field(env='ZMANIM_API_URL')
    GEO_API_URL: str = Field(env='GEO_API_URL')
    MAPBOX_API_KEY: str = Field(env='MAPBOX_API_KEY')

    REPORT_ADMIN_LIST: List[int] = Field(env='REPORT_ADMIN_LIST')

    LOCATION_NUMBER_LIMIT: int = Field(5, env='LOCATION_NUMBER_LIMIT')
    SENTRY_KEY: Optional[str] = Field(env='SENTRY_PUBLIC_KEY')

    METRICS_DSN: Optional[str] = Field(env='METRICS_DSN')
    METRICS_TABLE_NAME: Optional[str] = Field(env='METRICS_TABLE_NAME')

    PAYMENTS_PROVIDER_TOKEN: str = Field(env='PAYMENTS_PROVIDER_TOKEN')
    DONATE_OPTIONS: List[int] = Field([2, 5, 10, 25, 50])

    @validator('REPORT_ADMIN_LIST', pre=True)
    def parse_list(cls, report_admin_list):
        if isinstance(report_admin_list, int):
            return [report_admin_list]
        if isinstance(report_admin_list, str):
            return [int(i.strip()) for i in report_admin_list.split(',')]
        return report_admin_list


config = Config()
