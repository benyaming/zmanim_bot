from typing import Callable

from .types import Fast, FastData, SimpleDict
from .utils import gr_month_genitive, days_of_week


def get_translate(data: dict, _: Callable) -> Fast:
    """
    input data structure:
    {
        'fast_name': str,
        'date': {       !!!DATE OF EVE OF THE FAST!!!
            'day': int,
            'month': int,
            'year': int,
            'dow': int
        },
        'fast': {
            'start_time': str,
            'hatzot': Optional[str],
            'tzeit_time': str,
            'sba_time': str,
            'nvr_time': str,
            'ssk_time': str
        }
    }
    """
    titles = {
        'fast_gedaliah': _('FAST OF GEDALIAH'),
        '10_tevet': _('10 OF TEVET'),
        'fast_esther': _('FAST OF ESTHER'),
        '17_tammuz': _('17 OF TAMMUZ'),
        '9_av': _('9 OF AV'),
    }

    title = titles.get(data['fast_name'])

    fast_data: dict = data['fast']

    day: int = data["date"]["day"]
    month = gr_month_genitive.get(data["date"]["month"])
    year: int = data["date"]["year"]
    dow = days_of_week.get(data['date']['dow'])

    start_time = f'{day} {month} {year}\n{dow}, {fast_data["start_time"]}'

    if data['fast']['hatzot']:
        hatzot = SimpleDict(_('Hatzot'), fast_data['hatzot'])
    else:
        hatzot = None

    translated_data = Fast(title=title, data=FastData(
        start_time=SimpleDict(_('The fast begins'), start_time),
        tzeit_kochavim=SimpleDict(_('Tzeit akochavim'), fast_data['tzeit_time']),
        sba_time=SimpleDict(_('Sefer ben ashmashot'), fast_data['sba_time']),
        nvr_time=SimpleDict(_('Nevareshet'), fast_data['nvr_time']),
        ssk_time=SimpleDict(_('Shmirat shabbat keilhata'), fast_data['ssk_time']),
        hatzot=hatzot,
    ))

    return translated_data
