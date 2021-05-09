import asyncio
import logging
from typing import Tuple

import data
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import exceptions, executor
from pymongo import MongoClient

from zmanim_bot import config

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

texts = {
    'ru': data.ru_message,
    'en': data.en_message
}
button_texts = {
    'ru': data.ru_button_text,
    'en': data.en_button_text
}


def get_users() -> Tuple[int, str]:
    client = MongoClient(config.DB_URL)
    collection = client[config.DB_NAME][config.DB_COLLECTION_NAME]
    docs = list(collection.find())
    users = map(lambda doc: (doc['user_id'], doc['language']), docs)
    yield from users


async def send_message(
        user_id: int,
        text: str,
        kb: InlineKeyboardMarkup = None,
        disable_notification: bool = False
) -> bool:
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification, reply_markup=kb)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster() -> int:
    """
    Simple broadcaster
    :return: Count of messages
    """
    count = 0
    try:
        for user_id, lang in get_users():
            text = texts.get(lang)
            if text is None:
                log.error(f'There is no known language for user {user_id}')
                continue

            kb = InlineKeyboardMarkup()
            kb.row(InlineKeyboardButton(text=button_texts[lang], url=data.link))
            if await send_message(user_id, text, kb=kb):
                count += 1
            await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        log.info(f"{count} messages successful sent.")

    return count


if __name__ == '__main__':
    # Execute broadcaster
    executor.start(dp, broadcaster())
