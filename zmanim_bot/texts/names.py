# from ..middlewares.i18n import i18n_
#
# _ = i18n_.lazy_gettext
# __ = i18n_.gettext
_ = lambda x: x
__ = lambda x, y: (x, y)


MONTH_NAMES_GENETIVE = {
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

WEEKDAYS_GENETIVE = {
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

# Time units
tu_year = _('year')
tu_month = __('month', 'months')
tu_day = __('day', 'days')
tu_hour = __('hour', 'hours')
tu_minute = __('minute', 'minutes')
tu_part = __('part', 'parts')

and_word = _('and')



