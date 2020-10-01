from typing import Dict

from babel.support import LazyProxy

from ...middlewares.i18n import lazy_gettext as _


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

TORAH_PARTS = {
    'bereishis': _('bereishis'),
    'noach': _('noach'),
    'lech_lecha': _('lech_lecha'),
    'vayeira': _('vayeira'),
    'chayei_sarah': _('chayei_sarah'),
    'toldos': _('toldos'),
    'vayeitzei': _('vayeitzei'),
    'vayishlach': _('vayishlach'),
    'vayeishev': _('vayeishev'),
    'mikeitz': _('mikeitz'),
    'vayigash': _('vayigash'),
    'vayechi': _('vayechi'),
    'shemos': _('shemos'),
    'vaeirah': _('vaeirah'),
    'bo': _('bo'),
    'beshalach': _('beshalach'),
    'yisro': _('yisro'),
    'mishpatim': _('mishpatim'),
    'terumah': _('terumah'),
    'tetzaveh': _('tetzaveh'),
    'ki_sisa': _('ki_sisa'),
    'vayakheil': _('vayakheil'),
    'pekudei': _('pekudei'),
    'vayikra': _('vayikra'),
    'tzav': _('tzav'),
    'shemini': _('shemini'),
    'tazria': _('tazria'),
    'metzora': _('metzora'),
    'acharei': _('acharei'),
    'kedoshim': _('kedoshim'),
    'emor': _('emor'),
    'behar': _('behar'),
    'bechukosai': _('bechukosai'),
    'bamidbar': _('bamidbar'),
    'naso': _('naso'),
    'behaalosecha': _('behaalosecha'),
    'shelach': _('shelach'),
    'korach': _('korach'),
    'chukas': _('chukas'),
    'balak': _('balak'),
    'pinchas': _('pinchas'),
    'matos': _('matos'),
    'masei': _('masei'),
    'devarim': _('devarim'),
    'vaeschanan': _('vaeschanan'),
    'eikev': _('eikev'),
    'reei': _('reei'),
    'shoftim': _('shoftim'),
    'ki_seitzei': _('ki_seitzei'),
    'ki_savo': _('ki_savo'),
    'nitzavim': _('nitzavim'),
    'vayeilech': _('vayeilech'),
    'haazinu': _('haazinu'),
    'vezos_haberacha': _('vezos_haberacha'),

    'vayakheil - pikudei': _('vayakheil - pikudei'),
    'tazria - metzora': _('tazria - metzora'),
    'acharei - kedoshim': _('acharei - kedoshim'),
    'behar - bechukosai': _('behar - bechukosai'),
    'chukas - balak': _('chukas - balak'),
    'matos - masei': _('matos - masei'),
    'nitzavim - vayeilech': _('nitzavim - vayeilech'),
    
    'rosh_hashana': _('shabbat_rosh_hashana'),
    'yom_kippur': _('shabbat_yom_kippur'),
    'succos': _('shabbat_succos'),
    'chol_hamoed_succos': _('shabbat_chol_hamoed_succos'),
    'hoshana_rabbah': _('shabbat_hoshana_rabbah'),
    'shemini_atzeres': _('shabbat_shemini_atzeres'),
    'simchas_torah': _('shabbat_simchas_torah'),
    'pesach': _('shabbat_pesach'),
    'chol_hamoed_pesach': _('shabbat_chol_hamoed_pesach'),
    'shavuos': _('shabbat_shavuos')
}

GEMARA_BOOKS = {
    'Brachos': _('Brachos'),
    'Shabbos': _('Shabbos'),
    'Eruvin': _('Eruvin'),
    'Pesachim': _('Pesachim'),
    'Shekalim': _('Shekalim'),
    'Yoma': _('Yoma'),
    'Sukah': _('Sukah'),
    'Beitzah': _('Beitzah'),
    'Rosh Hashana': _('Rosh Hashana'),
    'Taanis': _('Taanis'),
    'Megilah': _('Megilah'),
    'Moed Katan': _('Moed Katan'),
    'Chagigah': _('Chagigah'),
    'Yevamos': _('Yevamos'),
    'Kesuvos': _('Kesuvos'),
    'Nedarim': _('Nedarim'),
    'Nazir': _('Nazir'),
    'Sotah': _('Sotah'),
    'Gitin': _('Gitin'),
    'Kidushin': _('Kidushin'),
    'Bava Kama': _('Bava Kama'),
    'Bava Metzia': _('Bava Metzia'),
    'Bava Basra': _('Bava Basra'),
    'Sanhedrin': _('Sanhedrin'),
    'Makos': _('Makos'),
    'Shevuos': _('Shevuos'),
    'Avodah Zarah': _('Avodah Zarah'),
    'Horayos': _('Horayos'),
    'Zevachim': _('Zevachim'),
    'Menachos': _('Menachos'),
    'Chulin': _('Chulin'),
    'Bechoros': _('Bechoros'),
    'Erchin': _('Erchin'),
    'Temurah': _('Temurah'),
    'Kerisos': _('Kerisos'),
    'Meilah': _('Meilah'),
    'Nidah': _('Nidah')
}
