from typing import Tuple
from datetime import date

from zmanim.hebrew_calendar.jewish_date import JewishDate

from .texts.single.names import JEWISH_MONTHS_GENETIVE
from .exceptions import IncorrectLocationException, IncorrectGregorianDateException


LOCATION_PATTERN = r'^-?\d{1,2}\.{1}\d+, {0,1}-?\d{1,3}\.{1}\d+$'
LANGUAGE_SHORTCUTS = {
    'English': 'en',
    'Русский': 'ru'
}
CALL_ANSWER_OK = '✅'

CL_OFFET_OPTIONS = [10, 15, 18, 20, 22, 30, 40]
HAVDALA_OPINION_OPTIONS = [
    'tzeis_5_95_degrees',
    'tzeis_8_5_degrees',
    'tzeis_42_minutes',
    'tzeis_72_minutes',
]


class CallbackPrefixes:
    cl = 'cl:'
    zmanim = 'zmanim_api:'
    havdala = 'havdala:'
    report = 'report:'
    zmanim_by_date = 'zbd:'
    omer = 'omer:'


def parse_coordinates(coordinates: str) -> Tuple[float, float]:
    try:
        lat, lng = map(float, coordinates.split(','))
    except ValueError:
        raise IncorrectLocationException('Incorrect location format!')

    if lng > 180.0 or lng < -180.0 or lat > 90.0 or lat < -90.0:
        raise IncorrectLocationException('Incorrect location value!')

    return lat, lng


def parse_date(date_: str) -> str:
    try:
        date.fromisoformat(date_)
    except ValueError:
        raise IncorrectGregorianDateException
    return date_


def parse_jewish_date(date_str: str) -> str:
    year, month, day = date_str.split('-')
    return f'{day} {JEWISH_MONTHS_GENETIVE.get(list(JewishDate.MONTHS)[int(month) - 1].name)} {year}'
