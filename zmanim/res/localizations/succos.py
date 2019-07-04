from typing import Callable

from .types import SuccosData, Succos, GenericData
from .utils import gr_month_genitive as gr, days_of_week as dow, date_header, \
    cl_header, cl_shabbos, hvd_header, hoshana_raba_header


def get_translate(data: dict, _: Callable) -> Succos:
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
        'hoshana_raba': {
            'day': int,
            'month': int,
            'dow': int
        },
    }

    hr = hoshana raba
    cl = candle lighting
    """
    title = _('SUCCOS')

    eve_day = data['day_1']['eve_day']
    eve_month = gr.get(data['day_1']['eve_month'])
    day_start = data['day_1']['day']
    day_hr = data['hoshana_raba']['day']
    dow_start = dow.get(data['day_1']['dow'])
    dow_hr = dow.get(data['hoshana_raba']['dow'])
    month_start = gr.get(data['day_1']['month'])
    month_hr = gr.get(data['hoshana_raba']['month'])

    date_months = f'{day_start}-{day_hr} {month_start}' if month_start == month_hr \
        else f'{day_start} {month_start}-{day_hr} {month_hr}'

    date_str = f'{date_months} {data["year"]},\n{dow_start}-{dow_hr}'

    day_1, day_2, day_3 = data['day_1'], data['day_2'], data['day_3']
    shabbos = f' ({cl_shabbos})'

    cl_1_header = f'{cl_header} {eve_day} {eve_month}'
    if data['day_1']['dow'] == 5:
        cl_1_header = f'{cl_1_header}{shabbos}'

    cl_2 = None
    if day_2:
        # eve of second day == first day
        cl_2_header = f'{cl_header} {day_start} {month_start}'
        cl_2 = GenericData(cl_2_header, day_2['cl'])

    cl_3 = None
    if day_3:
        # eve of third day == second day
        cl_3_header = f'{cl_header} {day_2["day"]} {gr.get(day_2["month"])}{shabbos}'
        cl_3 = GenericData(cl_3_header, day_3["cl"])

    # havdala
    if day_3:
        havdala_header_str = f'{hvd_header} {day_3["day"]} {gr.get(day_3["month"])}'
        havdala = GenericData(havdala_header_str, day_3['havdala'])
    elif day_2:
        havdala_header_str = f'{hvd_header} {day_2["day"]} {gr.get(day_2["month"])}'
        havdala = GenericData(havdala_header_str, day_2['havdala'])
    else:
        havdala_header_str = f'{hvd_header} {day_1["day"]} {gr.get(day_1["month"])}'
        havdala = GenericData(havdala_header_str, day_1['havdala'])

    hr_data = data['hoshana_raba']
    hoshana_raba_value = f'{hr_data["day"]} {gr.get(hr_data["month"])}, ' \
                         f'{dow.get(hr_data["dow"])}'

    translated_data = Succos(
        title=title,
        data=SuccosData(
            date=GenericData(date_header, date_str),
            candle_lighting_1=GenericData(cl_1_header, day_1['cl']),
            candle_lighting_2=cl_2,
            candle_lighting_3=cl_3,
            havdala=havdala,
            hoshana_raba=GenericData(hoshana_raba_header, hoshana_raba_value)
        )
    )

    return translated_data
