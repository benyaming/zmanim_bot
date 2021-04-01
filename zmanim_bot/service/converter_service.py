from datetime import date
from typing import Tuple

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar

from zmanim_bot import keyboards
from zmanim_bot.exceptions import IncorrectJewishDateException, IncorrectGregorianDateException
from zmanim_bot.keyboards.inline import get_zmanim_by_date_buttons
from zmanim_bot.states import ConverterGregorianDateState, ConverterJewishDateState
from zmanim_bot.texts.single import messages
from zmanim_bot.texts.single.names import MONTH_NAMES_GENETIVE, WEEKDAYS, JEWISH_MONTHS_GENETIVE


def get_converter_entry_menu() -> Tuple[str, ReplyKeyboardMarkup]:
    kb = keyboards.menus.get_converter_menu()
    return messages.init_converter, kb


async def init_greg_to_jew() -> Tuple[str, ReplyKeyboardMarkup]:
    await ConverterGregorianDateState().waiting_for_gregorian_date.set()
    kb = keyboards.menus.get_cancel_keyboard()
    return messages.greg_date_request, kb


async def init_jew_to_greg() -> Tuple[str, ReplyKeyboardMarkup]:
    await ConverterJewishDateState().waiting_for_jewish_date.set()
    kb = keyboards.menus.get_cancel_keyboard()
    return messages.jew_date_request, kb


def convert_heb_to_greg(date_: str) -> Tuple[str, InlineKeyboardMarkup]:
    try:
        year, month, day = map(int, date_.split('-'))
    except ValueError:
        raise IncorrectJewishDateException

    try:
        calendar = JewishCalendar(year, month, day)
    except ValueError:
        raise IncorrectJewishDateException
    gr_date = calendar.gregorian_date
    resp = f'{gr_date.day} {MONTH_NAMES_GENETIVE[gr_date.month]} {gr_date.year}, {WEEKDAYS[gr_date.weekday()]}'

    kb = get_zmanim_by_date_buttons([gr_date])
    return resp, kb


def convert_greg_to_heb(date_: str) -> Tuple[str, InlineKeyboardMarkup]:
    try:
        pydate = date.fromisoformat(date_)
    except ValueError:
        raise IncorrectGregorianDateException

    calendar = JewishCalendar.from_date(pydate)
    jewish_date = f'{calendar.jewish_day} {JEWISH_MONTHS_GENETIVE[calendar.jewish_month_name()]} {calendar.jewish_year},' \
                  f' {WEEKDAYS[calendar.gregorian_date.weekday()]}'
    kb = get_zmanim_by_date_buttons([pydate])
    return jewish_date, kb

