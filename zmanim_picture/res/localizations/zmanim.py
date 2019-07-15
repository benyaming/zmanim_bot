from typing import Callable

from .types import Zmanim


def get_translate(data: dict, _: Callable) -> Zmanim:
    """
    input data structure:
    {
        'date': {
            'gr': [dd, mm, yy],
            'he': [dd, 'mm', yy],
        },
        'zmanim_picture': {
            'zman_name': '...',
            ...
            ...
        }
    }
    """
    title = _('ZMANIM')
    zman_names = {
        'sunrise': _('sunrise'),
        'sof_zman_tefila_gra': _('sof_zman_tefila_gra'),
        'sof_zman_tefila_ma': _('sof_zman_tefila_ma'),
        'talis_ma': _('talis_ma'),
        'sof_zman_shema_gra': _('sof_zman_shema_gra'),
        'sof_zman_shema_ma': _('sof_zman_shema_ma'),
        'chatzos': _('chatzos'),
        'mincha_ketana_gra': _('mincha_ketana_gra'),
        'mincha_gedola_ma': _('mincha_gedola_ma'),
        'alot_ma': _('alot_ma'),
        'plag_mincha': _('plag_mincha'),
        'sunset': _('sunset'),
        'tzeis_850d': _('tzeis_850d'),
        'tzeis_rt': _('tzeis_rt'),
        'tzeis_42m': _('tzeis_42m'),
        'tzeis_595d': _('tzeis_595d'),
        'chatzos_laila': _('chatzos_laila'),
        'astronomical_hour_ma': _('astronomical_hour_ma'),
        'astronomical_hour_gra': _('astronomical_hour_gr')
    }
    months_gr_genetive = {
        1: _('january-genetive'),
        2: _('february-genetive'),
        3: _('march-genetive'),
        4: _('april-genetive'),
        5: _('may-genetive'),
        6: _('june-genetive'),
        7: _('july-genetive'),
        8: _('august-genetive'),
        9: _('september-genetive'),
        10: _('october-genetive'),
        11: _('november-genetive'),
        12: _('december-genetive'),
    }
    months_he_ginitive = {
        'Nisan': _('nisan-genetive'),
        'Iyar': _('iyar-genetive'),
        'Sivan': _('sivan-genetive'),
        'Tamuz': _('tamuz-genetive'),
        'Av': _('av-genetive'),
        'Elul': _('elul-genetive'),
        'Tishrei': _('tishrei-genetive'),
        'Cheshvan': _('cheshvan-genetive'),
        'Kislev': _('kislev-genetive'),
        'Teves': _('teves-genetive'),
        'Shevat': _('shevat-genetive'),
        'Adar': _('adar-genetive'),
        'Adar I': _('adar I-genetive'),
        'Adar II': _('adar II-genetive'),
    }

    gr_date: list = data['date']['gr']
    he_date: list = data['date']['he']
    date = f'{gr_date[0]} {months_gr_genetive.get(gr_date[1])} {gr_date[2]}/' \
           f'{he_date[0]} {months_he_ginitive.get(he_date[1])} {gr_date[2]}'

    translated_data = Zmanim(
        title=title, date=date,
        zmanim={zman_names.get(k): v for k, v in data['zmanim_picture'].items()}
    )

    return translated_data
