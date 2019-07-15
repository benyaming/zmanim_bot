import re
from datetime import datetime as dt

from zmanim_bot.texts import hebrew_months
from zmanim_bot.converter import convert_heb_to_greg


DATE_RE_PATTERN = r'^[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,4}$'
INCORRECT = 'incorrect date format'
NOT_EXIST = 'date not exist'
OK = 'ok'


def handle_gregorian_date(raw_date: str) -> str:
    """
    Handles gregorian date that has been imputed by user and checks if it correct
    and exist
    :param raw_date: date string inputed by user
    """
    extracted_date = re.search(DATE_RE_PATTERN, raw_date)
    if not extracted_date:
        return INCORRECT

    day, month, year = map(int, extracted_date.group().split('.'))
    try:
        dt(year=year, month=month, day=day)
    except ValueError:
        return NOT_EXIST

    return OK


def day_validation(day: str) -> str:
    """Validates that day inputed by digits and it's lenght not more then 31"""
    validated = OK
    if not day.isdigit():
        validated = INCORRECT
    day = int(day)
    if not 0 < day < 31:
        validated = INCORRECT
    return validated


def month_validation(month: str) -> str:
    """Validates that name of the month is correct"""
    month = month.lower()
    return OK if month in hebrew_months else INCORRECT


def year_validation(year: str) -> str:
    """Validates that year inputed by digits and it in CE"""
    validated = OK
    if not year.isdigit():
        validated = INCORRECT
    year = int(year)
    if not 0 < year < 9999:
        validated = INCORRECT
    return validated


def handle_hebrew_date(raw_date: str) -> str:
    """
    Handles hebrew date that has been imputed by user and checks if it correct
    and exist
    :param raw_date: date string inputed by user, ex '1 tammuz 5777' OR '1 adar II 5777'
    """
    date = raw_date.split()
    if len(date) not in (3, 4):  # check number of words/digits
        return INCORRECT

    day = date[0]
    month = date[1] if len(date) == 3 else f'{date[1]} {date[2]}'
    year = date[-1]

    day_status = day_validation(day)
    if day_status != OK:
        return day_status

    year_status = year_validation(year)
    if year_status != OK:
        return year_status

    month_status = month_validation(month)
    if month_status != OK:
        return month_status

    converted_date = convert_heb_to_greg(date, '')


    return ''
