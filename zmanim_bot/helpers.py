from datetime import date
from typing import Tuple

from .exceptions import IncorrectGregorianDateException, IncorrectLocationException

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
    location_activate = 'loc_a:'
    location_rename = 'loc_r:'
    location_delete = 'loc_d:'


def parse_coordinates(coordinates: str) -> Tuple[float, float]:
    try:
        lat, lng = map(float, coordinates.split(','))
    except ValueError:
        raise IncorrectLocationException('Incorrect location format!')

    if lng > 180.0 or lng < -180.0 or lat > 90.0 or lat < -90.0:
        raise IncorrectLocationException('Incorrect location value!')

    return lat, lng


def check_date(date_: str):
    try:
        date.fromisoformat(date_)
    except ValueError:
        raise IncorrectGregorianDateException
