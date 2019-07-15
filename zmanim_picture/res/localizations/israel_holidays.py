from typing import Callable

from .types import GenericData, IsraelHoliday, IsraelHolidays
from .utils import gr_month_genitive as gr, days_of_week as dow, date_header, \
    israel_holidays_names


def get_translate(data: dict, _: Callable) -> IsraelHolidays:
    """
    input data schema:
    {
        'year': int,
        'yom_hashoa': {
            'day': int,
            'month': int,
            'dow': int
        },
        'yom_hazikaron': {
            'day': int,
            'month': int,
            'dow': int
        },
        'yom_haatzmaut': {
            'day': int,
            'month': int,
            'dow': int
        },
        'yom_yerushalaim': {
            'day': int,
            'month': int,
            'dow': int
        },
    }
    """
    title = _('ISRAEL_HOLIDAYS')
    year = data['year']
    yom_hashoah = data['yom_hashoa']
    yom_hazikaron = data['yom_hazikaron']
    yom_haatzmaut = data['yom_haatzmaut']
    yom_yerushalaim = data['yom_yerushalaim']

    yom_hashoah_date = f'{yom_hashoah["day"]} {gr.get(yom_hashoah["month"])} {year}, ' \
                       f'{dow.get(yom_hashoah["dow"])}'
    yom_hazikaron_date = f'{yom_hazikaron["day"]} {gr.get(yom_hazikaron["month"])} ' \
                         f'{year}, {dow.get(yom_hazikaron["dow"])}'
    yom_haatzmaut_date = f'{yom_haatzmaut["day"]} {gr.get(yom_haatzmaut["month"])} ' \
                         f'{year}, {dow.get(yom_haatzmaut["dow"])}'
    yom_yerushalaim_date = f'{yom_yerushalaim["day"]} {gr.get(yom_yerushalaim["month"])} '\
                           f'{year}, {dow.get(yom_yerushalaim["dow"])}'

    yom_hashoah_title = israel_holidays_names.get('yom_hashoa')
    yom_hazikaron_title = israel_holidays_names.get('yom_hazikaron')
    yom_haatzmaut_title = israel_holidays_names.get('yom_haatzmaut')
    yom_yerushalaim_title = israel_holidays_names.get('yom_yerushalaim')

    yom_hashoah_date = GenericData(date_header, yom_hashoah_date)
    yom_hazikaron_date = GenericData(date_header, yom_hazikaron_date)
    yom_haatzmaut_date = GenericData(date_header, yom_haatzmaut_date)
    yom_yerushalaim_date = GenericData(date_header, yom_yerushalaim_date)

    translated_data = IsraelHolidays(
        title=title,
        yom_hashoa=IsraelHoliday(title=yom_hashoah_title, date=yom_hashoah_date),
        yom_hazikaron=IsraelHoliday(title=yom_hazikaron_title, date=yom_hazikaron_date),
        yom_haatzmaaut=IsraelHoliday(title=yom_haatzmaut_title, date=yom_haatzmaut_date),
        yom_yerushalaim=IsraelHoliday(title=yom_yerushalaim_title, date=yom_yerushalaim_date)
    )
    return translated_data
