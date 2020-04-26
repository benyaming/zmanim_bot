from aiogram.types import Update

from ..misc import dp
from .redirects import (
    redirect_to_request_location,
    redirect_to_request_language,
    incorrect_text_warning
)
from ..exceptions import (
    IncorrectLocationException,
    NoLocationException,
    NoLanguageException,
    IncorrectTextException
)


@dp.errors_handler(exception=NoLocationException)
async def no_location_exception_handler(update: Update, e: NoLocationException):
    await redirect_to_request_location()
    return True


@dp.errors_handler(exception=NoLanguageException)
async def no_language_exception_handler(update: Update, e: NoLanguageException):
    await redirect_to_request_language()
    return True


@dp.errors_handler(exception=IncorrectTextException)
async def no_language_exception_handler(update: Update, e: IncorrectTextException):
    await incorrect_text_warning()
    return True
