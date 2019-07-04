from typing import Callable

from .types import RoshHashana, RoshHashanaData, SimpleDict
from .utils import gr_month_genitive as gr, days_of_week as dow, and_word, cl_header


def get_translate(data: dict, _: Callable) -> RoshHashana:
    """
    input data schema:
    {
        'year': int,
        'day_1': {
            'candle_lighting': str,
            'eve_day': int,
            'eve_month': int,
            'day': int,
            'month': int,
            'dow': int
        },
        'day_2': {
            'candle_lighting': str,
            'havdala': Optional[str],
            'day': int,
            'month': int,
            'dow': int
        },
        'day_3': Optional[{
            'candle_lighting': str,
            'havdala': str,
            'day': int,
            'month': int,
            'dow': int
        }]
    }
    """
    title = _('ROSH HASHANA')
    hv_header = _('Havdala')
    shabbos = _('shabbos')

    eve_day = data['day_1']['eve_day']
    eve_month = gr.get(data['day_1']['eve_month'])
    day_1 = data['day_1']['day']
    day_2 = data['day_2']['day']
    dow_1 = dow.get(data['day_1']['dow'])
    dow_2 = dow.get(data['day_2']['dow'])
    month_1 = gr.get(data['day_1']['month'])
    month_2 = gr.get(data['day_2']['month'])

    months = f'{day_1} {month_1} {and_word} {day_2} {month_2}' if month_1 != month_2 \
        else f'{day_1} {and_word} {day_2} {month_1}'

    date_str = f'{months} {data["year"]},\n{dow_1}-{dow_2}'

    cl_1 = f"{cl_header} {eve_day} {eve_month}"
    # eve of second day == first day
    cl_2 = f"{cl_header} {day_1} {month_2}"

    havdala_date = f'{day_2} {month_2}' if not data['day_3'] \
        else f'{data["day_3"]["day"]} {gr.get(data["day_3"]["month"])}'
    havdala_header = f'{hv_header} {havdala_date}'

    if dow_1 == 6:
        cl_1 = f'{cl_1} ({shabbos})'

    day_3 = None
    havdala = SimpleDict(havdala_header, data['day_2']['havdala'])

    if data['day_3']:
        day_3_data = data['day_3']
        # eve of third day == second day
        cl_3 = f"{cl_header} {day_2} {gr.get(day_3_data['month'])} ({shabbos})"
        day_3 = SimpleDict(cl_3, day_3_data['candle_lighting'])
        havdala = SimpleDict(havdala_header, day_3_data['havdala'])

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
