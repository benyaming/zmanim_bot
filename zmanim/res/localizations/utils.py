"""
Some dicts with translated data used in localizatoin files
"""
from gettext import gettext as _


# gregorian months in genetive
gr_month_genitive = {
    1: _('january-genetive'),
    2: _('february-genetive'),
    3: _('march-genetive'),
    4: _('april-genetive'),
    5: _('may-genetive'),
    6: _('june-genetive'),
    7: _('july-genetive'),
    8: _('august-genetive'),
    9: _('septemberr'),
    10: _('octoberrr'),
    11: _('november-genetive'),
    12: _('december-genetive'),
}

# hebrew months
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

days_of_week = {
    0: _('monday'),
    1: _('tuesday'),
    2: _('wednesday'),
    3: _('thursday'),
    4: _('friday'),
    5: _('saturday'),
    6: _('sunday'),
}

and_word = _('and')
date_header = _('Date')
cl_header = _('Candle lighting')
cl_shabbos = _('shabbos')
havdala_header = _('Havdala')

# SUCCOS
hoshana_raba_header = _('Hoshana raba')

