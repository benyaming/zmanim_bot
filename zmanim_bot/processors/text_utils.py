from datetime import date, time
from typing import List, Union

from zmanim.hebrew_calendar.jewish_date import JewishDate

from zmanim_bot.integrations.zmanim_models import AsurBeMelachaDay
from zmanim_bot.texts.single import names
from zmanim_bot.texts.single.names import JEWISH_MONTHS_GENITIVE


def humanize_date(date_range: List[Union[date, AsurBeMelachaDay]],
                  weekday_on_new_line: bool = False) -> str:
    """
    Use this function for humanize date or date range
    Examples:
      2020-01-01 -> 1 January 2020, Wednesday
      2020-01-01, 2020-01-08 -> 1—7 January 2020, Wednesday-Tuesday
      2020-01-31, 2020-02-1 -> 31 January—1 February 2020, Friday-Saturday
      2019-12-25, 2020-01-03 -> 25 December 2019—3 January 2020, Wednesday-Friday
    """
    weekday_sep = '\n' if weekday_on_new_line else ' '
    months = names.MONTH_NAMES_GENETIVE
    weekdays = names.WEEKDAYS

    d1 = date_range[0]
    d2 = date_range[1] if (len(date_range) > 1) and (date_range[0] != date_range[1]) else None

    if isinstance(d1, AsurBeMelachaDay):
        d1 = d1.date
    if isinstance(d2, AsurBeMelachaDay):
        d2 = d2.date

    if not d2:
        d = d1
        resp = f'{d.day} {months[d.month]} {d.year},{weekday_sep}{weekdays[d.weekday()]}'

    elif d1.year != d2.year:
        resp = f'{d1.day} {months[d1.month]} {d1.year} — ' \
               f'{d2.day} {months[d2.month]} {d2.year}, ' \
               f'{weekdays[d1.weekday()]}-{weekdays[d2.weekday()]}'

    elif d1.month != d2.month:
        resp = f'{d1.day} {months[d1.month]} — {d2.day} {months[d2.month]} {d1.year},{weekday_sep}' \
               f'{weekdays[d1.weekday()]}-{weekdays[d2.weekday()]}'

    else:
        resp = f'{d1.day}-{d2.day} {months[d1.month]} {d1.year},{weekday_sep}' \
               f'{weekdays[d1.weekday()]}-{weekdays[d2.weekday()]}'

    return resp


def humanize_time(time_: time) -> str:
    """ Use this function for convert time to hh:mm """
    if isinstance(time_, time):
        return time_.isoformat(timespec='minutes')


def parse_jewish_date(date_str: str) -> str:
    year, month, day = date_str.split('-')
    return f'{day} {JEWISH_MONTHS_GENITIVE.get(list(JewishDate.MONTHS)[int(month) - 1].name)} {year}'
