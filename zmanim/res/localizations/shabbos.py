from typing import Callable

from os import path
from gettext import translation


def get_translate(data: dict, _: Callable) -> dict:
    """
    input data structure:
    {
        'parasha': '...',
        'candle_lighting': '...|None',
        'shkia_offset': '...(int)|None',
        'tzeit_kochavim': '...|None'
        'error': True|False,
        'warning': True|False
    }

    output data structure (words in `` are translated):
    {
        'title': `...`,
        data: {
            'parasha': {
                'parasha_header': `...`,
                'parasha_value': `...`
            },
            'candle_lighting': {
                'candle_lighting_header': `...`,
                'candle_lighting_value': '...'
            } | None,
            'shkia_offset': `...`| None,
            'tzeit_kochavim': {
                'tzeit_header': `...`,
                'tzeit_value': '...'
            } | None,
            'warning': `...`|None,
            'error': `...`|None
        }
    }
    """

    parashiyot = {
        'Bereshit': _('Bereshit'),
        'Noach': _('Noach'),
        'Lech Lecha': _('Lech Lecha'),
        'Vayerah': _('Vayerah'),
        'Chayei Sarah': _('Chayei Sarah'),
        'Toldot': _('Toldot'),
        'Vayeitzei': _('Vayeitzei'),
        'Vayishlach': _('Vayishlach'),
        'Vayeishev': _('Vayeishev'),
        'Mikeitz': _('Mikeitz'),
        'Vayigash': _('Vayigash'),
        'Vayechi': _('Vayechi'),
        'Shemot': _('Shemot'),
        'Vaeira': _('Vaeira'),
        'Bo': _('Bo'),
        'Beshalach': _('Beshalach'),
        'Yitro': _('Yitro'),
        'Mishpatim': _('Mishpatim'),
        'Terumah': _('Terumah'),
        'Tetzaveh': _('Tetzaveh'),
        'Ki Tisa': _('Ki Tisa'),
        'Vayakhel-Pekudei': _('Vayakhel-Pekudei'),
        'Vayakhel': _('Vayakhel'),
        'Pekudei': _('Pekudei'),
        'Vayikra': _('Vayikra'),
        'Tzav': _('Tzav'),
        'Shemini': _('Shemini'),
        'Tazria-Metzorah': _('Tazria-Metzorah'),
        'Tazria': _('Tazria'),
        'Metzorah': _('Metzorah'),
        'Acharei Mot-Kedoshim': _('Acharei Mot-Kedoshim'),
        'Acharei Mot': _('Acharei Mot'),
        'Kedoshim': _('Kedoshim'),
        'Emor': _('Emor'),
        'Behar-Bechukotai': _('Behar-Bechukotai'),
        'Behar': _('Behar'),
        'Bechukotai': _('Bechukotai'),
        'Bamidbar': _('Bamidbar'),
        'Naso': _('Naso'),
        'Beha\'alotecha': _('Beha\'alotecha'),
        'Shelach': _('Shelach'),
        'Korach': _('Korach'),
        'Chukat': _('Chukat'),
        'Balak': _('Balak'),
        'Pinchas': _('Pinchas'),
        'Matot-Masei': _('Matot-Masei'),
        'Matot': _('Matot'),
        'Masei': _('Masei'),
        'Devarim': _('Devarim'),
        'Va\'etchanan': _('Va\'etchanan'),
        'Eikev': _('Eikev'),
        'Re\'eh': _('Re\'eh'),
        'Shoftim': _('Shoftim'),
        'Ki Teitzei': _('Ki Teitzei'),
        'Ki Tavo': _('Ki Tavo'),
        'Nitzavim-Vayeilech': _('Nitzavim-Vayeilech'),
        'Nitzavim': _('Nitzavim'),
        'Vayeilech': _('Vayeilech'),
        'Ha\'azinu': _('Ha\'azinu'),
        # TODO add holyday shabbos
    }

    title = _('SHABBOS')
    parasha_header = _('Parashat ha-shavua')
    parasha_value = parashiyot.get(data['parasha'])
    candle_lighting_header = _('Candle lighting')
    shkia_offset_header = _('minutes before shekiah')
    tzeit_header = _('Tzeit ha-kochavim')

    if data['error']:
        error = _('For this location zmanim is impossible\nto determine because of '
                  'polar night/day.')
    else:
        error = None

    if data['warning']:
        warning = _('Notice! You should specify time of candle\n lighting with the ' 
                    'rabbi of your community!')
    else:
        warning = None

    translated_data = {
        'title': title,
        'data': {
            'parasha': {
                'parasha_header': parasha_header,
                'parasha_value': parasha_value
            },
            'candle_lighting': {
                'candle_lighting_header': candle_lighting_header,
                'candle_lighting_value': data['candle_lighting']
            },
            'shkia_offset': f'({data["shkia_offset"]} {shkia_offset_header})',
            'tzeit_kochavim': {
                'tzeit_header': tzeit_header,
                'tzeit_value': data['tzeit_kochavim']
            },
            'warning': warning,
            'error': error
        }
    }

    return translated_data


t = {
    'parasha': 'Bo',
    'candle_lighting': '11:11',
    'shkia_offset': 18,
    'tzeit_kochavim': '22:22',
    'error': False,
    'warning': False
    }


# def get_translator(domain: str, lang: str) -> Callable:
#     languages = {'Russian': 'ru', 'English': 'en'}
#     loc_path = path.join(r'C:\Users\Benyomin\PycharmProjects\zmanim_api\zmanim', 'locales/')
#     locale = translation(domain, loc_path, languages=[languages.get(lang)])
#     locale.install()
#     return locale.gettext
#
#
# f = get_translator('shabbos', 'Russian')
# a = get_translate(t, f)
#
# import pprint
# pprint.pprint(a)



