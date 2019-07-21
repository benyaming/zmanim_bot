from typing import Tuple

from pyluach.dates import GregorianDate, HebrewDate
from pyluach.hebrewcal import Month, Year


def convert_heb_to_greg(date: Tuple[int, str, int], lang: str) -> str:
    day, month, year = date


def convert_greg_to_heb(date: Tuple[int, str, int], lang: str) -> str:
    day, month, year = date
    hebrew_date = GregorianDate(year=year, month=month, day=day).to_heb()

