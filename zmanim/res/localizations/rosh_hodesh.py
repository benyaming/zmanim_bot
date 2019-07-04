from typing import Callable

from .types import RoshHodesh, SimpleDict, RHData, RHDate, RHMolad
from .utils import he_months, gr_month_genitive, days_of_week


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

    rh_date = RHDate(
        header=_('Date'),
        days=[str(i) for i in data['date']['date_days']],
        months=[gr_month_genitive.get(i) for i in data['date']['date_months']],
        years=[str(i) for i in data['date']['date_years']],
        dow=[days_of_week.get(i) for i in data['date']['date_dow']]
    )

    molad = RHMolad(
        header=_('Molad'),
        day=data['molad']['molad_day'],
        month=gr_month_genitive.get(data['molad']['molad_month']),
        dow=days_of_week.get(data['molad']['molad_dow']),
        n_hours=data['molad']['molad_hour'],
        hours_word=hours.get(data['molad']['molad_hour'] % 10),
        n_of_minutes=data['molad']['molad_minutes'],
        minutes_word=minutes.get(data['molad']['molad_minutes'] % 10),
        and_word=and_word,
        n_parts=data['molad']['molad_parts'],
        parts_word=parts.get(data['molad']['molad_parts'] % 10)
    )

    translated_data = RoshHodesh(
        title=title, data=RHData(
            SimpleDict(_('Month'), he_month),
            SimpleDict(_('Number of days'), data['n_days']),
            rh_date,
            molad
        )
    )

    return translated_data
