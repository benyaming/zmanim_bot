from typing import Dict

from babel.support import LazyProxy

from ...zmanim_api.models import *
from zmanim_bot.texts.translators import lazy_gettext as _


MONTH_NAMES_GENETIVE: Dict[int, LazyProxy] = {
    1: _('january-g'),
    2: _('fubruary-g'),
    3: _('march-g'),
    4: _('april-g'),
    5: _('may-g'),
    6: _('june-g'),
    7: _('july-g'),
    8: _('august-g'),
    9: _('september-g'),
    10: _('october-g'),
    11: _('november-g'),
    12: _('december-g'),
}

WEEKDAYS_GENETIVE: Dict[int, LazyProxy] = {
    0: _('monday-g'),
    1: _('tuesday-g'),
    2: _('wednesday-g'),
    3: _('thursday-g'),
    4: _('friday-g'),
    5: _('saturday-g'),
    6: _('sunday-g')
}

WEEKDAYS: Dict[int, LazyProxy] = {
    0: _('monday'),
    1: _('tuesday'),
    2: _('wednesday'),
    3: _('thursday'),
    4: _('friday'),
    5: _('saturday'),
    6: _('sunday')
}

# Titles
title_daf_yomi = _('DAF YOMI')
title_rosh_chodesh = _('ROSH CHODESH')
title_shabbath = _('SHABBAT')
title_zmanim = _('ZMANIM')
FASTS_TITLES = {
    'fast_gedalia': _('FAST OF GEDALIAH'),
    'fast_10_teves': _('FAST 10th OF TEVETH'),
    'fast_esther': _('FAST OF ESTHER'),
    'fast_17_tammuz': _('FAST 17th OF TAMMUZ'),
    'fast_9_av': _('FAST 9th OF AV')
}
HOLIDAYS_TITLES = {
    'chanukah': _('CHANUKAH'),
    'tu_bi_shvat': _('TU BI-SHVAT'),
    'purim': _('PURIM'),
    'lag_baomer': _('LAG BA-OMER'),
    'israel_holidays': _('ISRAEL HOLIDAYS')
}
YOMTOVS_TITLES = {
    'rosh_hashana': _('ROSH HA-SHANA'),
    'yom_kippur': _('YOM KIPUR'),
    'succot': _('SUCCOT'),
    'shmini_atzeres': _('SHMINI ATZERES'),
    'pesach': _('PESACH'),
    'shavuot': _('SHAVUOT')
}

shabbat = _('shabbat')






