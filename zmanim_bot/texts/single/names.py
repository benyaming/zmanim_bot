from typing import Dict

from babel.support import LazyProxy

from zmanim_bot.middlewares.i18n import lazy_gettext as _


MONTH_NAMES_GENETIVE: Dict[int, LazyProxy] = {
    # NOTE Genative month name
    1: _('January'),
    # NOTE Genative month name
    2: _('February'),
    # NOTE Genative month name
    3: _('March'),
    # NOTE Genative month name
    4: _('April'),
    # NOTE Genative month name
    5: _('May'),
    # NOTE Genative month name
    6: _('June'),
    # NOTE Genative month name
    7: _('July'),
    # NOTE Genative month name
    8: _('August'),
    # NOTE Genative month name
    9: _('September'),
    # NOTE Genative month name
    10: _('October'),
    # NOTE Genative month name
    11: _('November'),
    # NOTE Genative month name
    12: _('December'),

}

WEEKDAYS: Dict[int, LazyProxy] = {
    0: _('Monday'),
    1: _('Tuesday'),
    2: _('Wednesday'),
    3: _('Thursday'),
    4: _('Friday'),
    5: _('Saturday'),
    6: _('Sunday')
}

# Titles
title_daf_yomi = _('DAF YOMI')
title_rosh_chodesh = _('ROSH CHODESH')
title_shabbath = _('SHABBAT')
title_zmanim = _('ZMANIM')
FASTS_TITLES = {
    'fast_gedalia': _('FAST OF GEDALIAH'),
    'fast_10_teves': _('10th OF TEVET'),
    'fast_esther': _('FAST OF ESTHER'),
    'fast_17_tammuz': _('17th OF TAMMUZ'),
    'fast_9_av': _('9th OF AV')
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
    'shmini_atzeres': _('SHMINI ATZERET'),
    'pesach': _('PESACH'),
    'shavuot': _('SHAVUOT')
}

shabbat = _('shabbat')

TORAH_PARTS = {
    'bereishis': _('Bereshit'),
    'noach': _('Noach'),
    'lech_lecha': _('Lech-Lecha'),
    'vayeira': _('Vayeira'),
    'chayei_sarah': _('Chayei Sarah'),
    'toldos': _('Toledot'),
    'vayeitzei': _('Vayetze'),
    'vayishlach': _('Vayishlach'),
    'vayeishev': _('Vayeshev'),
    'mikeitz': _('Miketz'),
    'vayigash': _('Vayigash'),
    'vayechi': _('Vayechi'),
    'shemos': _('Shemot'),
    'vaeirah': _('Va\'eira'),
    'bo': _('Bo'),
    'beshalach': _('Beshalach'),
    'yisro': _('Yitro'),
    'mishpatim': _('Mishpatim'),
    'terumah': _('Terumah'),
    'tetzaveh': _('Tetzaveh'),
    'ki_sisa': _('Ki Tisa'),
    'vayakheil': _('Vayakhel'),
    'pekudei': _('Pekudei'),
    'vayikra': _('Vayikra'),
    'tzav': _('Tzav'),
    'shemini': _('Shemini'),
    'tazria': _('Tazria'),
    'metzora': _('Metzora'),
    'acharei': _('Acharei Mot'),
    'kedoshim': _('Kedoshim'),
    'emor': _('Emor'),
    'behar': _('Behar'),
    'bechukosai': _('Bechukotai'),
    'bamidbar': _('Bamidbar'),
    'naso': _('Naso'),
    'behaalosecha': _('Behaalotecha'),
    'shelach': _('Shlach'),
    'korach': _('Korach'),
    'chukas': _('Chukat'),
    'balak': _('Balak'),
    'pinchas': _('Pinchas'),
    'matos': _('Matot'),
    'masei': _('Masei'),
    'devarim': _('Devarim'),
    'vaeschanan': _('Va\'etchanan'),
    'eikev': _('Eikev'),
    'reei': _('Re\'eh'),
    'shoftim': _('Shoftim'),
    'ki_seitzei': _('Ki Teitzei'),
    'ki_savo': _('Ki Tavo'),
    'nitzavim': _('Nitzavim'),
    'vayeilech': _('Vayelech'),
    'haazinu': _('Haazinu'),
    'vezos_haberacha': _('V\'Zot HaBerachah'),

    'vayakheil - pikudei': _('Vayakhel - Pekudei'),
    'tazria - metzora': _('Tazria - Metzora'),
    'acharei - kedoshim': _('Acharei Mot - Kedoshim'),
    'behar - bechukosai': _('Behar - Bechukotai'),
    'chukas - balak': _('Chukat - Balak'),
    'matos - masei': _('Matot - Masei'),
    'nitzavim - vayeilech': _('Nitzavim - Vayelech'),
    
    'rosh_hashana': _('Shabbat Rosh ha-Shana'),
    'yom_kippur': _('Shabbat Yom Kippur'),
    'succos': _('Shabat Succot'),
    'chol_hamoed_succos': _('Shabbat Chol ha-moed Succot'),
    'hoshana_rabbah': _('Shabbat Chol ha-moed Succot'),
    'shemini_atzeres': _('Shabbat Shmini Atzeret'),
    'simchas_torah': _('Shabbat Simchat Torah'),
    'pesach': _('Shabbat Pesach'),
    'chol_hamoed_pesach': _('Shabbat Chol ha-moed Pesach'),
    'shavuos': _('Shabbat Shavuot')
}

GEMARA_BOOKS = {
    'berachos': _('Brachot'),
    'shabbos': _('Shabbat'),
    'eruvin': _('Eruvin'),
    'pesachim': _('Pesachim'),
    'shekalim': _('Shekalim'),
    'yoma': _('Yoma'),
    'sukkah': _('Sukah'),
    'beitzah': _('Beitzah'),
    'rosh_hashanah': _('Rosh Hashana'),
    'taanis': _('Taanit'),
    'megillah': _('Megilah'),
    'moed_katan': _('Moed Katan'),
    'chagigah': _('Chagigah'),
    'yevamos': _('Yevamot'),
    'kesubos': _('Kesuvot'),
    'nedarim': _('Nedarim'),
    'nazir': _('Nazir'),
    'sotah': _('Sotah'),
    'gitin': _('Gitin'),
    'kiddushin': _('Kidushin'),
    'bava_kamma': _('Bava Kama'),
    'bava_metzia': _('Bava Metzia'),
    'bava_basra': _('Bava Batra'),
    'sanhedrin': _('Sanhedrin'),
    'makkos': _('Makot'),
    'shevuos': _('Shevuot'),
    'avodah_zarah': _('Avodah Zarah'),
    'horiyos': _('Horayot'),
    'zevachim': _('Zevachim'),
    'menachos': _('Menachot'),
    'chullin': _('Chulin'),
    'bechoros': _('Bechorot'),
    'arachin': _('Erchin'),
    'temurah': _('Temurah'),
    'kerisos': _('Kerisot'),
    'meilah': _('Meilah'),
    'kinnim': _('Kinnim'),
    'tamid': _('Tamid'),
    'midos': _('Midot'),
    'niddah': _('Nidah')
}

JEWISH_MONTHS = {
    # NOTE It is very important to add space after the month name!!
    'nissan': _('Nisan '),
    # NOTE It is very important to add space after the month name!!
    'iyar': _('Iyar '),
    # NOTE It is very important to add space after the month name!!
    'sivan': _('Sivan '),
    # NOTE It is very important to add space after the month name!!
    'tammuz': _('Tammuz '),
    # NOTE It is very important to add space after the month name!!
    'av': _('Av '),
    # NOTE It is very important to add space after the month name!!
    'elul': _('Elul '),
    # NOTE It is very important to add space after the month name!!
    'tishrei': _('Tishrei '),
    # NOTE It is very important to add space after the month name!!
    'cheshvan': _('Cheshvan '),
    # NOTE It is very important to add space after the month name!!
    'kislev': _('Kislev '),
    # NOTE It is very important to add space after the month name!!
    'teves': _('Tevet '),
    # NOTE It is very important to add space after the month name!!
    'shevat': _('Shevat '),
    # NOTE It is very important to add space after the month name!!
    'adar': _('Adar '),
    # NOTE It is very important to add space after the month name!!
    'adar_ii': _('Adar II '),
}

JEWISH_MONTHS_GENETIVE = {
    # NOTE Genative month name
    'nissan': _('Nisan'),
    # NOTE Genative month name
    'iyar': _('Iyar'),
    # NOTE Genative month name
    'sivan': _('Sivan'),
    # NOTE Genative month name
    'tammuz': _('Tammuz'),
    # NOTE Genative month name
    'av': _('Av'),
    # NOTE Genative month name
    'elul': _('Elul'),
    # NOTE Genative month name
    'tishrei': _('Tishrei'),
    # NOTE Genative month name
    'cheshvan': _('Cheshvan'),
    # NOTE Genative month name
    'kislev': _('Kislev'),
    # NOTE Genative month name
    'teves': _('Tevet'),
    # NOTE Genative month name
    'shevat': _('Shevat'),
    # NOTE Genative month name
    'adar': _('Adar'),
    # NOTE Genative month name
    'adar_ii': _('Adar II'),
}
