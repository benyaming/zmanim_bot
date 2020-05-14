from typing import Dict

from babel.support import LazyProxy

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

# Titles
title_daf_yomi = _('DAF YOMI')
title_rosh_chodesh = _('ROSH CHODESH')
title_shabbath = _('SHABBAT')






