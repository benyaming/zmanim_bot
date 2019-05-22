from typing import Callable


def get_translate(data: dict, _: Callable) -> dict:
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
        }
        'molad': {
          'molad_month': '...(int)',
          'molad_day': '...(int)',
          'molad_dow': '...(int)',
          'molad_hours': '...(int)',
          'molad_minutes': '...(int)',
          'molad_parts': '...(int)',
        }
    }

    output data structure (words in `` are translated):
    {
        'title': `...`,
        'data': {
            'month': {
                'month_word': `...`,
                'month_value': `...`
            }
            'nod': {
                'nod_word': `...`,
                'nod': (int)
            },
            'date': {
                'date_word': `...`,
                'date_days': ['...(int)'],
                'date_months': [`...`],
                'date_years': ['...(int)'],
                'date_dow': [`...`]
            },
            'molad': {
                'molad_word': `...`,
                'molad_day': '...(int)',
                'molad_month': `...`,
                'molad_dow': `...`,
                'molad_n_of_hours': '...(int)',
                'molad_hours_w': `...`,
                'molad_n_of_minutes': '...(int)',
                'molad_minutes_w': `...`,
                'molad_and-word': `...`,
                'molad_n_of_parts': '...(int)',
                'molad_parts_w': `...`,
            }
        }
    }
    """
    title = _('ROSH_HODESH')
    and_word = _('and')

    he_months = {
        'Nisan': _('Nisan'),
        'Nissan': _('Nissan'),
        'Iyar': _('Iyar'),
        'Sivan': _('Sivan'),
        'Tamuz': _('Tamuz'),
        'Av': _('Av'),
        'Elul': _('Elul'),
        'Tishrei': _('Tishrei'),
        'Cheshvan': _('Cheshvan'),
        'Kislev': _('Kislev'),
        'Teves': _('Teves'),
        'Shevat': _('Shevat'),
        'Adar': _('Adar'),
        'Adar I': _('Adar I'),
        'Adar II': _('Adar II'),
    }
    gr_month_genitive = {
        1: _('January'),
        2: _('February'),
        3: _('March'),
        4: _('April'),
        5: _('May'),
        6: _('June'),
        7: _('July'),
        8: _('August'),
        9: _('September'),
        10: _('October'),
        11: _('November'),
        12: _('December'),
    }
    days_of_week = {
        0: _('Monday'),
        1: _('Tuesday'),
        2: _('Wednesday'),
        3: _('Thursday'),
        4: _('Friday'),
        5: _('Saturday'),
        6: _('Sunday'),
        7: _('Monday'),
        8: _('Tuesday')
    }
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

    rh_date = {
        'date_word': _('Date'),
        'date_days': [i for i in data['date']['date_days']],
        'date_months': [gr_month_genitive.get(i) for i in data['date']['date_months']],
        'date_years': [i for i in data['date']['date_years']],
        'date_dow': [days_of_week.get(i) for i in data['date']['date_dow']]
    }

    molad = {
        'molad_word': _('Molad'),
        'molad_day': data['molad']['molad_day'],
        'molad_month': gr_month_genitive.get(data['molad']['molad_month']),
        'molad_dow': days_of_week.get(data['molad']['molad_dow']),
        'molad_n_of_hours': data['molad']['molad_hours'],
        'molad_hours_w': hours.get(data['molad']['molad_hours'] % 10),
        'molad_n_of_minutes': data['molad']['molad_minutes'],
        'molad_minutes_w': minutes.get(data['molad']['molad_minutes'] % 10),
        'molad_and-word': and_word,
        'molad_n_of_parts': data['molad']['molad_parts'],
        'molad_parts_w': parts.get(data['molad']['molad_parts'] % 10),
    }

    translated_data = {
        'title': title,
        'data': {
            'month': {
                'month_word': _('Month'),
                'month_value': he_month
            },
            'nod': {
                'nod_word': _('Number of days'),
                'nod_value': data['n_days']
            },
            'date': rh_date,
            'molad': molad
        }
    }

    return translated_data


example = {
    'he_month': 'Tamuz',
    'n_days': 2,
    'date': {
        'date_years': [2000, 2001],
        'date_months': [12, 1],
        'date_days': [31, 1],
        'date_dow': [6, 0],
    },
    'molad': {
        'molad_month': 7,
        'molad_day': 15,
        'molad_dow': 3,
        'molad_hours': 15,
        'molad_minutes': 46,
        'molad_parts': 2,
    }
}

#
# def get_translator(domain: str, lang: str) -> Callable:
#     languages = {'Russian': 'ru', 'English': 'en'}
#     loc_path = path.join(r'C:\Users\Benyomin\PycharmProjects\zmanim_api\zmanim', 'locales/')
#     locale = translation(domain, loc_path, languages=[languages.get(lang)])
#     locale.install()
#     return locale.gettext
#
#
# f = get_translator('rosh_hodesh', 'Russian')
# a = get_translate(t, f)
#
# import pprint
# pprint.pprint(a, indent=4)