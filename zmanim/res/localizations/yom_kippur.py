from typing import Callable

from .types import YomKippur, YomKippurData, SimpleDict
from .utils import gr_month_genitive, days_of_week, date_header


def get_translate(data: dict, _: Callable) -> YomKippur:
    """
    input data schema:
        {
            'date': {
                'year': int,
                'months': List[int],
                'days': List[int],     EVE AND THE DATE
                'dows': List[int]
            },
            'candle_lighting': str,
            'havdala': str
        }
    """
    title = _('YOM KIPPUR')
    cl_header = _('Candle lightning and the fast begins')
    havdala_header = _('Havdala and the fast ends')

    days = data['date']['days']
    months = [gr_month_genitive.get(i) for i in data['date']['months']]
    dows = [days_of_week.get(i) for i in data['date']['dows']]
    year = data['date']['year']

    date = f'{days[0]} {months[0]} {year}, {dows[0]}'
    candle_lighting = f'{days[0]} {months[0]}, {data["candle_lighting"]}'
    havdala = f'{days[-1]} {months[-1]}, {data["candle_lighting"]}'

    translated_data = YomKippur(
        title=title,
        data=YomKippurData(
            date=SimpleDict(date_header, date),
            candle_lighting=SimpleDict(cl_header, candle_lighting),
            havdala=SimpleDict(havdala_header, havdala)
        )
    )

    return translated_data

