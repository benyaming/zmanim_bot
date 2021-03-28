from ...middlewares.i18n import lazy_gettext as _


# Service
geobutton = _('send location')
cancel = _('cancel')
back = _('back')
done = _('Done')


# Main menu
mm_zmanim = _('zmanim')
mm_shabbat = _('shabbat')
mm_holidays = _('holidays')
mm_daf_yomi = _('daf yomi')
mm_rh = _('rosh chodesh')
mm_fasts = _('fast days')
mm_zmanim_by_date = _('zmanim by the date')
mm_converter = _('date converter')
mm_help = _('help')
mm_settings = _('settings')


# Help menu
hm_faq = _('F.A.Q.')
hm_report = _('report a bug')


# Settings menu
sm_zmanim = _('select zmanim')
sm_candle = _('candle lighting')
sm_havdala = _('havdala')
sm_lang = _('language')
sm_location = _('location')
sm_omer = _('omer')


# Holidays
hom_more = _('more...')
hom_main = _('main holidays')

hom_rosh_hashana = _('rosh ha-shanah')
hom_yom_kippur = _('yom kippur')
hom_succot = _('succos')
hom_shmini_atzeret = _('shmini atzeres')
hom_chanukah = _('chanukah')
hom_purim = _('purim')
hom_pesach = _('pesach')
hom_shavuot = _('shavuos')
hom_tu_bishvat = _('tu bi-Shvat')
hom_lag_baomer = _('lag ba-omer')
hom_israel = _('israel holidays')


# Fasts
fm_gedaliah = _('fast of Gedaliah')
fm_tevet = _('10 of Tevet')
fm_esther = _('fast of Esther')
fm_tammuz = _('17 of Tammuz')
fm_av = _('9 of Av')

HOLIDAYS = [hom_rosh_hashana, hom_yom_kippur, hom_succot, hom_shmini_atzeret, hom_chanukah,
            hom_purim, hom_pesach, hom_shavuot, hom_tu_bishvat, hom_lag_baomer, hom_israel]
NON_YOM_TOV_HOLIDAYS = [hom_chanukah, hom_purim, hom_tu_bishvat, hom_lag_baomer, hom_israel]
FASTS = [fm_gedaliah, fm_tevet, fm_esther, fm_tammuz, fm_av]


# converter
conv_greg_to_jew = _('greg to jew')
conv_jew_to_greg = _('jew to greg')

zmanim_for = _('Zmanim for')
