from pydantic import BaseSettings, Field, validator


class Config(BaseSettings):

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    I18N_DOMAIN: str = Field('zmanim_bot')
    BOT_TOKEN: str = Field(env='BOT_TOKEN')

    IS_PROD: bool = Field(False, env='IS_PROD')
    WEBHOOK_PATH: str = Field('/zmanim_bot', env='WEBHOOK_PATH')

    LANGUAGE_LIST: list[str] = Field(['English', 'Русский', 'עברית'])
    LANGUAGE_SHORTCUTS: dict[str, str] = Field({
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

    # Base URL of the companion zmanim_site deployment used as a Telegram Mini
    # App (e.g. https://zmanim.example). Unset = all mini-app features off.
    MINIAPP_URL: str | None = Field(None, env='MINIAPP_URL')
    # Polling (dev) mode has no webhook server, so the mini-app API gets its own
    # aiohttp server on this port. Unused in prod (routes join the webhook app).
    MINIAPP_DEV_API_PORT: int = Field(8080, env='MINIAPP_DEV_API_PORT')
    # The calendar site's Google OAuth **web** client id — the same public value
    # the site is built with. Only used to check the `aud` of an ID token before
    # handing back that account's sync key. Unset = Google sign-in refused.
    GOOGLE_CLIENT_ID: str | None = Field(None, env='GOOGLE_CLIENT_ID')
    # Whether to trust the X-Real-IP header for the per-IP rate limit on the
    # site sync endpoints. Set True ONLY when the reverse proxy sets X-Real-IP
    # to the real client (nginx `proxy_set_header X-Real-IP $remote_addr;`,
    # which overwrites any client value) — then the limit keys on the real
    # client. Default False uses the direct socket peer: unspoofable, but behind
    # a proxy that's the proxy's IP, i.e. one shared bucket, so set True in the
    # proxied production deployment AFTER confirming nginx sets the header.
    TRUST_PROXY_HEADERS: bool = Field(False, env='TRUST_PROXY_HEADERS')

    REPORT_ADMIN_LIST: list[int] = Field(env='REPORT_ADMIN_LIST')

    LOCATION_NUMBER_LIMIT: int = Field(5, env='LOCATION_NUMBER_LIMIT')
    SENTRY_KEY: str | None = Field(env='SENTRY_PUBLIC_KEY')

    METRICS_DSN: str | None = Field(env='METRICS_DSN')
    METRICS_TABLE_NAME: str | None = Field(env='METRICS_TABLE_NAME')

    PAYMENTS_PROVIDER_TOKEN: str = Field(env='PAYMENTS_PROVIDER_TOKEN')
    DONATE_OPTIONS: list[int] = Field([2, 5, 10, 25, 50])

    OPEN_TOPO_DATA_DB: str = Field(..., env='OPEN_TOPO_DATA_DB')

    @validator('REPORT_ADMIN_LIST', pre=True)
    def parse_list(cls, report_admin_list):
        if isinstance(report_admin_list, int):
            return [report_admin_list]
        if isinstance(report_admin_list, str):
            return [int(i.strip()) for i in report_admin_list.split(',')]
        return report_admin_list


config = Config()
