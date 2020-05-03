from typing import Tuple

from pydantic import BaseModel

from .exceptions import IncorrectLocationException


LOCATION_PATTERN = r'^-?\d{1,2}\.{1}\d+, {0,1}-?\d{1,3}\.{1}\d+$'
LANGUAGE_SHORTCUTS = {
    'English': 'en',
    'Русский': 'ru'
}
CALL_ANSWER_OK = '✅'


class CallbackPrefixes:
    cl = 'cl:'
    zmanim = 'zmanim:'


# class ZmanimSettings(BaseModel):
#     """
#     This class represents user's active zmanim set and should have same dignature as
#     database zmanim set and zmanim_api's zmanim_set
#     """
#     sunrise: bool = True
#     alos: bool = True
#     sof_zman_tefila_gra: bool = True
#     sof_zman_tefila_ma: bool = True
#     talis_ma: bool = True
#     sof_zman_shema_gra: bool = True
#     sof_zman_shema_ma: bool = True
#     chatzos: bool = True
#     mincha_ketana: bool = True
#     mincha_gedola: bool = True
#     plag_mincha: bool = True
#     sunset: bool = True
#     tzeis_850_degrees: bool = True
#     tzeis_72_minutes: bool = True
#     tzeis_42_minutes: bool = True
#     tzeis_595_degrees: bool = True
#     chatzot_laila: bool = True


def parse_coordinates(coordinates: str) -> Tuple[float, float]:
    try:
        lat, lng = map(float, coordinates.split(','))
    except ValueError:
        raise IncorrectLocationException('Incorrect location format!')  # todo txt

    if lng > 180.0 or lng < -180.0 or lat > 90.0 or lat < -90.0:
        raise IncorrectLocationException('Incorrect location value!')  # todo txt

    return lat, lng


