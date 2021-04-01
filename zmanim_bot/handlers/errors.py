from asyncio.tasks import create_task

from aiogram.types import Update, Message

from zmanim_bot.api.storage_api import get_or_create_user
from ..misc import dp, logger
from .redirects import *
from .warnings import *
from ..exceptions import *
from ..texts.single.messages import error_occured


@dp.errors_handler(exception=NoLocationException)
async def no_location_exception_handler(update: Update, e: NoLocationException):
    await redirect_to_request_location()
    return True


@dp.errors_handler(exception=NoLanguageException)
async def no_language_exception_handler(update: Update, e: NoLanguageException):
    await redirect_to_request_language()
    create_task(get_or_create_user())
    # return True


@dp.errors_handler(exception=IncorrectGregorianDateException)
async def gregorian_date_exception_handler(update: Update, e: IncorrectGregorianDateException):
    await incorrect_greg_date_warning()
    return True


@dp.errors_handler(exception=IncorrectJewishDateException)
async def jewish_date_exception_handler(update: Update, e: IncorrectJewishDateException):
    await incorrect_jew_date_warning()
    return True


@dp.errors_handler(exception=Exception)
async def main_errors_handler(update: Update, e: Exception):
    if e.__class__ in (NoLanguageException, NoLocationException, IncorrectTextException,
                       IncorrectGregorianDateException, IncorrectJewishDateException):
        return True
    msg = Message.get_current()
    await msg.reply(error_occured)
    logger.exception(e)
    return True



