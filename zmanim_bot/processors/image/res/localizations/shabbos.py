from typing import Callable

from .types import Shabos, ShabosData, GenericData


def get_translate(data: dict, _: Callable) -> Shabos:
    """
    input data structure:
    {
        'parasha': '...',
        'cl': '...|None',
        'cl_offset': '...(int)|None',
        'tzeit_kochavim': '...|None',
        'error': True|False,
        'warning': True|False
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

    error = _('For this location image is impossible\nto determine because of '
              'polar night/day.') if data['error'] else None
    warning = _('Notice! You should specify time of candle\n lighting with the ' 
                'rabbi of your community!') if data['warning'] else None

    shkia_offset = f'({data["cl_offset"]} {shkia_offset_header})'

    translated_data = Shabos(title=title, data=ShabosData(
        parasha=GenericData(parasha_header, parasha_value),
        cl=GenericData(candle_lighting_header, data['cl']),
        shkia_offset=shkia_offset,
        tzeit_kochavim=GenericData(tzeit_header, data['tzeit_kochavim']),
        warning=warning, error=error
    ))

    return translated_data
