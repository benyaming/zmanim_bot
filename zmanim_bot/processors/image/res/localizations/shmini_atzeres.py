from typing import Callable

from .types import GenericData, GenericYomTov, GenericYomTovData
from .utils import gr_month_genitive as gr, days_of_week as dow, date_header, cl_header,\
    cl_shabbos, hvd_header


def get_translate(data: dict, _: Callable) -> GenericYomTov:
    """
    input data schema:
    {
        'year': int,
        'day_1': {
            'eve_day': int,
            'eve_month': int,
            'day': int,
            'month': int,
            'dow': int,
            'cl': str,
            'havdala': Optional[str]
        },
        'day_2': Optional[{
            'day': int,
            'month': int,
            'dow': int,
            'cl': str,
            'havdala': Optional[str]
        }],
        'day_3': Optional[{
            'day': int,
            'month': int,
            'dow': int,
            'cl': str,
            'havdala': str
        }],
    }
    """
    day_1_data, day_2_data, day_3_data = data['day_1'], data['day_2'], data['day_3']
    title = _('SHMINI ATZERET/SIMCHAT TORAH')

    eve_day = day_1_data['eve_day']
    eve_month = gr.get(day_1_data['eve_month'])
    day_1 = day_1_data['day']
    day_2 = day_2_data['day'] if day_2_data else ''
    dow_1 = dow.get(day_1_data['dow'])
    dow_2 = dow.get(day_2_data['dow']) if day_2_data else ''
    month_1 = gr.get(day_1_data['month'])
    month_2 = gr.get(day_2_data['month']) if day_2_data else ''
    sep = '-' if day_2_data else ''

    date_months = f'{day_1}{sep}{day_2} {month_1}' if month_1 == month_2 or not month_2\
        else f'{day_1} {month_1}{sep}{day_2} {month_2}'
    date_str = f'{date_months} {data["year"]},\n{dow_1}{sep}{dow_2}'

    shabbos = f' ({cl_shabbos})'

    cl_1_header = f'{cl_header} {eve_day} {eve_month}'
    if day_1_data['dow'] == 5:
        cl_1_header = f'{cl_1_header}{shabbos}'

    cl_2 = None
    if day_2:
        # eve of second day == first day
        cl_2_header = f'{cl_header} {day_1} {month_1}'
        cl_2 = GenericData(cl_2_header, day_2_data['cl'])

    cl_3 = None
    if day_3_data:
        # eve of third day == second day
        cl_3_header = f'{cl_header} {day_2_data["day"]} ' \
                      f'{gr.get(day_2_data["month"])}{shabbos}'
        cl_3 = GenericData(cl_3_header, day_3_data["cl"])

    # havdala
    if day_3_data:
        havdala_header_str = f'{hvd_header} {day_3_data["day"]} ' \
                             f'{gr.get(day_3_data["month"])}'
        havdala = GenericData(havdala_header_str, day_3_data['havdala'])
    elif day_2:
        havdala_header_str = f'{hvd_header} {day_2_data["day"]} ' \
                             f'{gr.get(day_2_data["month"])}'
        havdala = GenericData(havdala_header_str, day_2_data['havdala'])
    else:
        havdala_header_str = f'{hvd_header} {day_1_data["day"]} ' \
                             f'{gr.get(day_1_data["month"])}'
        havdala = GenericData(havdala_header_str, day_1_data['havdala'])

    translated_data = GenericYomTov(
        title=title,
        data=GenericYomTovData(
            date=GenericData(date_header, date_str),
            cl_1=GenericData(cl_1_header, day_1_data['cl']),
            cl_2=cl_2,
            cl_3=cl_3,
            havdala=havdala
        )
    )

    return translated_data
