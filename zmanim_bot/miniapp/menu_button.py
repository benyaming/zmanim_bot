from aiogram.types import MenuButtonWebApp, WebAppInfo

from zmanim_bot.misc import bot, logger
from zmanim_bot.texts.single import buttons


async def update_menu_button(user_id: int, miniapp_url: str | None):
    """Point the chat's menu button at the personalized mini-app URL.

    Best-effort: a Telegram API hiccup here must never break the flow that
    triggered the refresh (e.g. /start), so failures are only logged.
    """
    if not miniapp_url:
        return
    try:
        await bot.set_chat_menu_button(
            chat_id=user_id,
            menu_button=MenuButtonWebApp(text=buttons.calendar_app.value, web_app=WebAppInfo(url=miniapp_url)),
        )
    except Exception as e:
        logger.warning('Failed to update menu button for %s: %s', user_id, e)
