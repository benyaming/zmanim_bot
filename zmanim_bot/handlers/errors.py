import sentry_sdk
from aiogram import Bot
from aiogram.types import User, Message

from zmanim_bot.exceptions import *
from zmanim_bot.handlers.utils.redirects import *
from zmanim_bot.handlers.utils.warnings import *
from zmanim_bot.misc import dp, logger
from zmanim_bot.texts.single import messages
from zmanim_bot.texts.single.helpers import cl_error_warning
from zmanim_bot.texts.single.messages import error_occured


@dp.errors_handler(exception=NoLocationException)
async def no_location_exception_handler(*_):
    await redirect_to_request_location()
    return True


@dp.errors_handler(exception=IncorrectLocationException)
async def no_location_exception_handler(*_):
    user = User.get_current()
    bot = Bot.get_current()
    await bot.send_message(user.id, messages.incorrect_locations_received)
    return True


@dp.errors_handler(exception=NonUniqueLocationException)
async def non_unique_location_exception_handler(*_):
    user = User.get_current()
    bot = Bot.get_current()
    await bot.send_message(user.id, messages.location_already_exists)
    return True


@dp.errors_handler(exception=NonUniqueLocationNameException)
async def non_unique_location_name_exception_handler(*_):
    user = User.get_current()
    bot = Bot.get_current()
    await bot.send_message(user.id, messages.location_name_already_exists)
    return True


@dp.errors_handler(exception=MaxLocationLimitException)
async def non_unique_location_name_exception_handler(*_):
    user = User.get_current()
    bot = Bot.get_current()
    await bot.send_message(user.id, messages.too_many_locations_error)
    return True


@dp.errors_handler(exception=NoLanguageException)
async def no_language_exception_handler(*_):
    await redirect_to_request_language()


@dp.errors_handler(exception=IncorrectGregorianDateException)
async def gregorian_date_exception_handler(*_):
    await incorrect_greg_date_warning()
    return True


@dp.errors_handler(exception=IncorrectJewishDateException)
async def jewish_date_exception_handler(*_):
    await incorrect_jew_date_warning()
    return True


@dp.errors_handler(exception=PolarCoordinatesException)
async def polar_coordinates_exception_handler(*_):
    await Message.get_current().reply(cl_error_warning.value.replace('\n', ' '))
    return True


@dp.errors_handler(exception=Exception)
async def main_errors_handler(_, e: Exception):
    if isinstance(e, ZmanimBotBaseException):
        return True
    user = User.get_current()
    bot = Bot.get_current()
    await bot.send_message(user.id, error_occured)

    logger.exception(e)

    sentry_sdk.capture_exception(e)
    return True
