from typing import Callable

from .types import RoshHashana, RoshHashanaData, SimpleDict
from .utils import gr_month_genitive, days_of_week, and_word, cl_header


def get_translate(data: dict, _: Callable) -> RoshHashana:
    """
    input data schema:
    {
        'date: {
            'year': int,
            'months': List[int],
            'days': List[int],
            'dows': List[int]
        },
        'day_1': {
            'candle_lighting': str
        },
        'day_2': {
            'candle_lighting': str,
            'havdala': Optional[str]
        },
        'day_3': Optional[{
            'candle_lighting': str,
            'havdala': str
        }]
    }
    """
    title = _('ROSH HASHANA')
    havdala_header = _('Havdala')
    shabbos = _('shabbos')

    date = data['date']
    dow_1 = days_of_week.get(date['dows'][0])
    dow_2 = days_of_week.get(date['dows'][1])

    month_1 = gr_month_genitive.get(date['months'][0])
    month_2 = gr_month_genitive.get(date['months'][-1])

    if month_1 != month_2:
        date_str = f"{date['days'][0]} {month_1} {and_word} {date['days'][1]} " \
                   f"{month_2} {date['year']},\n{dow_1}-{dow_2}"
    else:
        date_str = f"{date['days'][0]} {and_word} {date['days'][1]} {month_1} " \
                   f"{date['year']},\n{dow_1}-{dow_2}"

    cl_1 = f"{cl_header} {date['days'][0]} {month_1}"
    cl_2 = f"{cl_header} {date['days'][1]} {month_2}"

    havdala_header = f'{havdala_header} {date["days"][-1]} {month_2}'

    if date['dows'][0] == 6:
        cl_1 = f'{cl_1} ({shabbos})'

    if data['day_3']:
        cl_3 = f"{cl_header} {date['days'][2]} {month_2} ({shabbos})"
        day_3 = SimpleDict(cl_3, data['day_3']['candle_lighting'])
        havdala = SimpleDict(havdala_header, data['day_3']['havdala'])
    else:
        day_3 = None
        havdala = SimpleDict(havdala_header, data['day_2']['havdala'])

    translated_data = RoshHashana(
        title=title,
        data=RoshHashanaData(
            date=SimpleDict(_('Date'), date_str),
            candle_lighting_1=SimpleDict(cl_1, data['day_1']['candle_lighting']),
            candle_lighting_2=SimpleDict(cl_2, data['day_2']['candle_lighting']),
            candle_lighting_3=day_3,
            havdalah=havdala
        )
    )

    return translated_data
