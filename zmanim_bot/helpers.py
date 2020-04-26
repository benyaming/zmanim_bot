import re
import enum
from typing import Tuple

from aiogram.types import Message

from .exceptions import IncorrectLocationException


LOCATION_PATTERN = r'^-?\d{1,2}\.{1}\d+, {0,1}-?\d{1,3}\.{1}\d+$'
LANGUAGE_SHORTCUTS = {
    'English': 'en',
    'Русский': 'ru'
}


def parse_coordinates(coordinates: str) -> Tuple[float, float]:
    try:
        lat, lng = map(float, coordinates.split(','))
    except ValueError:
        raise IncorrectLocationException('Incorrect location format!')  # todo txt

    if lng > 180.0 or lng < -180.0 or lat > 90.0 or lat < -90.0:
        raise IncorrectLocationException('Incorrect location value!')  # todo txt

    return lat, lng


