"""Telegram Mini App integration: the companion zmanim_site running inside Telegram.

- urls: builds the personalized mini-app URL (locale + active location).
- menu_button: points a chat's menu button at that URL.
- auth: validates Mini App initData (stateless HMAC auth for the API).
- api: aiohttp sub-application the mini app calls to read/sync user settings.

Everything is gated on `config.MINIAPP_URL`; unset means all of it stays off.
"""

from .menu_button import update_menu_button
from .urls import build_miniapp_url

__all__ = ['build_miniapp_url', 'update_menu_button']
