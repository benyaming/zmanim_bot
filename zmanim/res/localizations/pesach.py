from typing import Callable

from .types import Pesach, PesachData, GenericYomTovData, GenericData
from .utils import gr_month_genitive as gr, days_of_week as dow, cl_header, \
    hvd_header, date_header


def get_translate(data: dict, _: Callable) -> Pesach:
    """
    input data scheme:
    {
        'year': int,
        'part_1': {
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
                'havdala': Optional[str]
            }],
        },
        'part_2': {
            ## SAME AS PART 1 ##
        }
    }
    """
    title = _('PESACH')
    shabbos = _(' (shabbos)')
    p_1, p_2 = data['part_1'], data['part_2']

    first_month = p_1['day_1']['month']

    last_month = p_2['day_1']['month']
    last_day = p_2['day_1']['day']
    last_dow = dow.get(p_2['day_1']['dow'])
    if p_2['day_3']:
        last_month = p_2['day_3']['month']
        last_day = p_2['day_3']['day']
        last_dow = dow.get(p_2['day_3']['dow'])
    elif p_2['day_2']:
        last_month = p_2['day_2']['month']
        last_day = p_2['day_2']['day']
        last_dow = dow.get(p_2['day_2']['dow'])

    if first_month == last_month:
        months = f'{p_1["day_1"]["day"]}-{last_day} {gr.get(first_month)}'
    else:
        months = f'{p_1["day_1"]["day"]} {gr.get(first_month)}-{last_day} ' \
            f'{gr.get(last_month)}'

    date = f'{months} {data["year"]},\n{dow.get(p_1["day_1"]["dow"])}-{last_dow}'

    # First part.
    # p_1_cl_1 == part 1 candle lighning at 1st day
    p_1_day_1, p_1_day_2, p_1_day_3 = p_1['day_1'], p_1['day_2'], p_1['day_3']

    p_1_cl_1 = f'{cl_header} {p_1_day_1["eve_day"]} {gr.get(p_1_day_1["eve_month"])}'
    if p_1_day_1['dow'] == 5:
        p_1_cl_1 = f'{p_1_cl_1}{shabbos}'

    p_1_cl_2 = None
    if p_1_day_2:
        # eve of second day == first day
        p_1_cl_2_header = f'{cl_header} {p_1_day_1["day"]} {gr.get(p_1_day_1["month"])}'
        p_1_cl_2 = GenericData(p_1_cl_2_header, p_1_day_2["cl"])

    p_1_cl_3 = None
    if p_1_day_3:
        # eve of third day == second day
        p_1_cl_3_header = f'{cl_header} {p_1_day_2["day"]} ' \
                          f'{gr.get(p_1_day_2["month"])}{shabbos}'
        p_1_cl_3 = GenericData(p_1_cl_3_header, p_1_day_3["cl"])

    if p_1_day_3:
        havdala_header_1 = f'{hvd_header} {p_1_day_3["day"]} {gr.get(p_1_day_3["month"])}'
        havdala_1 = GenericData(havdala_header_1, p_1_day_3["havdala"])
    elif p_1_day_2:
        havdala_header_1 = f'{hvd_header} {p_1_day_2["day"]} {gr.get(p_1_day_2["month"])}'
        havdala_1 = GenericData(havdala_header_1, p_1_day_2["havdala"])
    else:
        havdala_header_1 = f'{hvd_header} {p_1_day_1["day"]} {gr.get(p_1_day_1["month"])}'
        havdala_1 = GenericData(havdala_header_1, p_1_day_1["havdala"])

    # First part. p_1_cl_1 == part 1 candle lighning at 1st day
    p_2_day_1, p_2_day_2, p_2_day_3 = p_2['day_1'], p_2['day_2'], p_2['day_3']

    p_2_cl_1 = f'{cl_header} {p_2_day_1["eve_day"]} {gr.get(p_2_day_1["eve_month"])}'
    if p_2_day_1['dow'] == 5:
        p_2_cl_1 = f'{p_2_cl_1}{shabbos}'

    p_2_cl_2 = None
    if p_2_day_2:
        # eve of second day == first day
        p_2_cl_2_header = f'{cl_header} {p_2_day_1["day"]} {gr.get(p_2_day_1["month"])}'
        p_2_cl_2 = GenericData(p_2_cl_2_header, p_2_day_2["cl"])

    p_2_cl_3 = None
    if p_2_day_3:
        # eve of third day == second day
        p_2_cl_3_header = f'{cl_header} {p_2_day_2["day"]} ' \
            f'{gr.get(p_2_day_2["month"])}{shabbos}'
        p_2_cl_3 = GenericData(p_2_cl_3_header, p_2_day_3["cl"])

    if p_2_day_3:
        havdala_header_2 = f'{hvd_header} {p_2_day_3["day"]} {gr.get(p_2_day_3["month"])}'
        havdala_2 = GenericData(havdala_header_2, p_2_day_3["havdala"])
    elif p_2_day_2:
        havdala_header_2 = f'{hvd_header} {p_2_day_2["day"]} {gr.get(p_2_day_2["month"])}'
        havdala_2 = GenericData(havdala_header_2, p_2_day_2["havdala"])
    else:
        havdala_header_2 = f'{hvd_header} {p_2_day_1["day"]} {gr.get(p_2_day_1["month"])}'
        havdala_2 = GenericData(havdala_header_2, p_2_day_1["havdala"])

    translated_data = Pesach(
        title=title,
        data=PesachData(
            date=GenericData(date_header, date),
            part_1=GenericYomTovData(
                cl_1=GenericData(p_1_cl_1, p_1_day_1['cl']),
                cl_2=p_1_cl_2,
                cl_3=p_1_cl_3,
                havdala=havdala_1
            ),
            part_2=GenericYomTovData(
                cl_1=GenericData(p_2_cl_1, p_2_day_1['cl']),
                cl_2=p_2_cl_2,
                cl_3=p_2_cl_3,
                havdala=havdala_2
            )
        )
    )

    return translated_data
