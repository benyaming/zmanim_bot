from typing import Callable

from .types import GenericData, GenericHoliday
from .utils import gr_month_genitive as gr, days_of_week as dow, date_header


def get_translate(data: dict, _: Callable) -> GenericHoliday:
    """
    input data schema:
    {
        'start_date': {
            'day': int,
            'month': int,
            'year': int,
            'dow': int
        },
        'end_date': {
            'day': int,
            'month': int,
            'year': int,
            'dow': int
        }
    }
    """
    title = _('CHANNUKAH')

    start_day, end_day = data['start_date']['day'], data['end_date']['day']
    start_month = gr.get(data['start_date']['month'])
    end_month = gr.get(data['end_date']['month'])
    start_year, end_year = data['start_date']['year'], data['end_date']['year']
    start_dow = dow.get(data['end_date']['dow'])
    end_dow = dow.get(data['start_date']['dow'])

    if start_year != end_year:
        date = f'{start_day} {start_month} {start_year}-\n' \
               f'{end_day} {end_month} {end_year},\n{start_dow}-{end_dow}'
    elif start_month != end_month:
        date = f'{start_day} {start_month}-{end_day} {end_month} {start_year},\n' \
               f'{start_dow}-{end_dow}'
    else:
        date = f'{start_day}-{end_day} {start_month} {start_year},\n' \
               f'{start_dow}-{end_dow}'

    translated_data = GenericHoliday(title=title, date=GenericData(date_header, date))
    return translated_data
