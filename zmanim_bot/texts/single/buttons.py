from zmanim_bot.middlewares.i18n import lazy_gettext as _

# Service
cancel = _('Cancel')
back = _('Back')
done = _('Done')

# location
geobutton = _('Send location')
search_location = _('Find location by name')
manage_locations = _('Manage saved locations')
add_location = _('Add new location')


# Main menu
mm_zmanim = _('Zmanim')
mm_shabbat = _('Shabbat')
mm_holidays = _('Holidays')
mm_daf_yomi = _('Daf yomi')
mm_rh = _('Rosh chodesh')
mm_fasts = _('Fast days')
mm_zmanim_by_date = _('Zmanim by the date')
mm_converter = _('Date converter')
mm_help = _('Help')
mm_settings = _('Settings')
mm_donate = _('Donate')


# Help menu
hm_faq = _('F.A.Q.')
hm_report = _('Report a problem')


# Settings menu
sm_zmanim = _('Select zmanim')
sm_candle = _('Candle lighting')
sm_havdala = _('Havdala')
sm_lang = _('Language')
sm_location = _('Location')
sm_omer = _('Omer count')
sm_format = _('Format')
sm_format_text_option = _('Text')
sm_format_image_option = _('Picture')

processor_types = {
    'image': sm_format_image_option,
    'text': sm_format_text_option,
}

settings_enabled = _('enabled')
settings_disabled = _('disabled')

# Holidays
hom_more = _('More...')
hom_main = _('Main holidays')

hom_rosh_hashana = _('Rosh ha-Shanah')
hom_yom_kippur = _('Yom Kippur')
hom_succot = _('Succot')
hom_shmini_atzeret = _('Shmini Atzeres')
hom_chanukah = _('Chanukah')
hom_purim = _('Purim')
hom_pesach = _('Pesach')
hom_shavuot = _('Shavuot')
hom_tu_bishvat = _('Tu bi-Shvat')
hom_lag_baomer = _('Lag ba-Omer')
hom_israel = _('Israel holidays')


# Fasts
fm_gedaliah = _('Fast of Gedaliah')
fm_tevet = _('10th of Tevet')
fm_esther = _('Fast of Ester')
fm_tammuz = _('17th of Tammuz')
fm_av = _('9th of Av')

YOMTOVS = [hom_rosh_hashana, hom_yom_kippur, hom_succot, hom_shmini_atzeret, hom_pesach, hom_shavuot]
HOLIDAYS = [hom_chanukah, hom_purim, hom_tu_bishvat, hom_lag_baomer, hom_israel]
FASTS = [fm_gedaliah, fm_tevet, fm_esther, fm_tammuz, fm_av]


# converter
conv_greg_to_jew = _('Gregorian ➡ Jewish')
conv_jew_to_greg = _('Jewish ➡ Gregorian')

# NOTE prefix for button "Zmanim for {date}"
zmanim_for_date_prefix = _('Zmanim for')
