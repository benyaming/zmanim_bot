from zmanim_bot.middlewares.i18n import lazy_gettext as _


init_bot = _('welcome to Zmanim bot!')
init_main_menu = _('Welcome to the main menu!')
init_help = _('how can I help you?')
init_settings = _('welcome to settings!')
init_report = _('describe your problem')
init_converter = _('welcome to converter, select:')
select = _('choose')


request_language = _('request language')
request_location = _('request location')

incorrect_text = _('Incorrect command. Please, choose one of the options on the buttons')
incorrect_greg_date = _('Incorrect gregorian date... plz try again')
incorrect_jew_date = _('Incorrect/Illegal date format. Take a look at the correct one: \n<code>YYYY-MM-DD\n'
                       '1 Nisan\n'
                       '2 Iyar\n'
                       '3 Sivan\n'
                       '4 Tammuz\n'
                       '5 Av\n'
                       '6 Elul\n'
                       '7 Tishrei\n'
                       '8 Cheshvan\n'
                       '9 Kislev\n'
                       '10 Tevet\n'
                       '11 Shvat\n'
                       '12 Adar/Adar\n'
                       '13 Adar II</code>')

settings_cl = _('select cl offset')
settings_zmanim = _('select zmanim')
settings_havdala = _('select havdala')
settings_omer = _('Here you can enable or disable notifications about the <i>Omer</i> count.')
settings_enabled = _('enabled')
settings_disabled = _('disabled')

greg_date_request = _('input gregorian date in ISO format')
jew_date_request = _('Please enter Jewish date in following format: \n<code>YYYY-MM-DD\n'
                     '1 Nisan\n'
                     '2 Iyar\n'
                     '3 Sivan\n'
                     '4 Tammuz\n'
                     '5 Av\n'
                     '6 Elul\n'
                     '7 Tishrei\n'
                     '8 Cheshvan\n'
                     '9 Kislev\n'
                     '10 Tevet\n'
                     '11 Shvat\n'
                     '12 Adar/Adar\n'
                     '13 Adar II</code>')

reports_text_received = _('your message successfully received. if you want, you can attach some '
                          'screenshots. when you will finish, press "Done"')
reports_media_received = _('Screenshot succesfully received.')
reports_incorrect_media_type = _('Incorrect media type. Please, send your screenshot as photo.')
reports_created = _('your report had ben sent to admin, you will receive notification with status')

error_occured = _('Looks like an error occured... The Bot\'s developer already working on it...')
