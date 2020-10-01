from datetime import date

from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar

from ..texts.single.names import JEWISH_MONTHS_GENETIVE, MONTH_NAMES_GENETIVE, WEEKDAYS
from ..exceptions import IncorrectGregorianDateException, IncorrectJewishDateException


def convert_heb_to_greg(date_: str) -> str:
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
    return resp


def convert_greg_to_heb(date_: str) -> str:
    try:
        pydate = date.fromisoformat(date_)
    except ValueError:
        raise IncorrectGregorianDateException

    calendar = JewishCalendar.from_date(pydate)
    jewish_date = f'{calendar.jewish_day} {JEWISH_MONTHS_GENETIVE[calendar.jewish_month_name()]} {calendar.jewish_year},' \
                  f' {WEEKDAYS[calendar.gregorian_date.weekday()]}'
    return jewish_date

