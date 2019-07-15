from typing import Callable

from .types import GenericData, GenericHoliday
from .utils import gr_month_genitive as gr, days_of_week, date_header


def get_translate(data: dict, _: Callable) -> GenericHoliday:
    """
    input data schema:
    {
        'day': int,
        'month': int,
        'year': int,
        'dow': int
    }
    """
    title = _('PURIM')

    day = data['day']
    month = gr.get(data['month'])
    year = data['year']
    dow = days_of_week.get(data['dow'])

    date = f'{day} {month} {year},\n{dow}'

    translated_data = GenericHoliday(title=title, date=GenericData(date_header, date))
    return translated_data
