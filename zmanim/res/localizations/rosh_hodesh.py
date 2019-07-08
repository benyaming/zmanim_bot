from typing import Callable

from .types import RoshHodesh, GenericData, RHData
from .utils import he_months, gr_month_genitive, days_of_week, date_header


def get_translate(data: dict, _: Callable) -> RoshHodesh:
    """
    input data structure:
    {
        'he_month': '...',
        'n_days': '...(int)',
        'date': {
          'date_years': [...(int)],
          'date_months': [...(int)],
          'date_days': [...(int)],
          'date_dow': [...(int)],
        },
        'molad': {
          'molad_month': '...(int)',
          'molad_day': '...(int)',
          'molad_dow': '...(int)',
          'molad_hour': '...(int)',
          'molad_minutes': '...(int)',
          'molad_parts': '...(int)',
        }
    }
    """
    title = _('ROSH_HODESH')
    and_word = _('and')
    molad_header = _('Molad')

    hours = {
        1: _('Hour-1'),
        2: _('Hour-2'),
        3: _('Hour-3'),
        4: _('Hour-4'),
        5: _('Hour-5'),
        6: _('Hour-6'),
        7: _('Hour-7'),
        8: _('Hour-8'),
        9: _('Hour-9'),
        0: _('Hour-0'),
    }
    minutes = {
        1: _('Minute-1'),
        2: _('Minute-2'),
        3: _('Minute-3'),
        4: _('Minute-4'),
        5: _('Minute-5'),
        6: _('Minute-6'),
        7: _('Minute-7'),
        8: _('Minute-8'),
        9: _('Minute-9'),
        0: _('Minute-0'),
    }
    parts = {
        1: _('Part-1'),
        2: _('Part-2'),
        3: _('Part-3'),
        4: _('Part-4'),
        5: _('Part-5'),
        6: _('Part-6'),
        7: _('Part-7'),
        8: _('Part-8'),
        9: _('Part-9'),
        0: _('Part-0'),
    }

    he_month = he_months.get(data['he_month'])

    date_days = [str(i) for i in data['date']['date_days']]
    date_months = [gr_month_genitive.get(i) for i in data['date']['date_months']]
    date_years = [str(i) for i in data['date']['date_years']]
    date_dows = [days_of_week.get(i) for i in data['date']['date_dow']]
    new_line = '\n' if len(date_days) > 1 else ' '

    date_day = f'{date_days[0]}' if len(date_days) == 1 \
        else f'{date_days[0]}-{date_days[1]}'
    date_month = f'{date_months[0]}' if len(date_months) == 1 \
        else f'{date_months[0]}-{date_months[1]}'
    date_year = f'{date_years[0]}' if len(date_years) == 1 \
        else f'{date_years[0]}-{date_years[1]}'
    date_dow = f'{date_dows[0]}' if len(date_dows) == 1 \
        else f'{date_dows[0]}-{date_dows[1]}'

    date_value = f'{date_day} {date_month} {date_year},{new_line}{date_dow}'

    molad_day = data['molad']['molad_day']
    molad_month = gr_month_genitive.get(data['molad']['molad_month'])
    molad_dow = days_of_week.get(data['molad']['molad_dow'])
    molad_n_hours = data['molad']['molad_hour']
    molad_hours_word = hours.get(data['molad']['molad_hour'] % 10)
    molad_n_of_minutes = data['molad']['molad_minutes']
    molad_minutes_word = minutes.get(data['molad']['molad_minutes'] % 10)
    molad_n_parts = data['molad']['molad_parts']
    molad_parts_word = parts.get(data['molad']['molad_parts'] % 10)

    molad_value = f'{molad_day} {molad_month}, {molad_dow},\n{molad_n_hours} ' \
                  f'{molad_hours_word} {molad_n_of_minutes} {molad_minutes_word} ' \
                  f'{and_word} {molad_n_parts} {molad_parts_word}'

    translated_data = RoshHodesh(
        title=title, data=RHData(
            month=GenericData(_('Month'), he_month),
            n_days=GenericData(_('Number of days'), data['n_days']),
            date=GenericData(date_header, date_value),
            molad=GenericData(molad_header, molad_value)
        )
    )

    return translated_data
