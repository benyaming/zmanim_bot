from zmanim_bot.middlewares.i18n import lazy_gettext as _


init_bot = _('Welcome to zmanim bot!')
init_main_menu = _('You are in the main menu:')
init_help = _('How can I help you?')
init_settings = _('You are in the settings:')
init_report = _('Please, describe your problem:')
init_converter = _('Choose the way of conversion:')
select = _('Choose:')

settings_cl = _('How long before shkiya do you light candles?')
settings_zmanim = _('Select zmanim that you want to receive:')
settings_havdala = _('Select your opinion for havdala:')
settings_omer = _('Here you can enable or disable notifications about the <i>Omer</i> count.')
settings_location = _('Here you can activate, edit or send new location:')

request_language = _('Select your language:')

request_location = _('Please share your location by pressing the button.\n'
                     '<b>Warning!</b> Desktop version of Telegram doesn’t support this type of '
                     'location sharing. To share you location from PC/Mac send them in comma '
                     'separated text (example: <code>55.5, 37.7</code>) or send a geotag message here.')
incorrect_locations_received = _('You sent incorrect coordinates. Please check and re-send them!')
location_already_exists = _('This location alredy exists in your saved locations!')
location_name_already_exists = _('This location name alredy exists in your saved locations!')
too_many_locations_error = _('You saved too many locations, please remove some of them before saving new one!')
custom_location_name_request = _('Automatic location name: {}.\n'
                                 'You can write custom name for the location or press "Done" button.')
location_deleted = _('Location successfully deleted!')
location_renamed = _('Location successfully renamed!')
location_saved = _('Location successfully saved!')
unable_to_delete_active_location = _('It is unable to delete active location!')
location_new_name_request = _('Please, write here new location name for {}:')
location_activated = _('{} selected!')

incorrect_text = _('"I’m not aware of such command 🤖\nWould you choose something from the menu:')


greg_date_request = _('Please enter Gregorian date in following format: <code>YYYY-MM-DD</code>')
incorrect_greg_date = _('Incorrect/Illegal date format. Take a look at the correct one: '
                        '<code>YYYY-MM-DD</code>')
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


reports_text_received = _('Your message has been saved for sending. You can attach screenshots or '
                          'videos of your choice. Once done, click the Done button.')
reports_media_received = _('File added successfully. Add another one or click Done.')
reports_incorrect_media_type = _('Unsupported message format. You can attach screenshots or videos '
                                 'by sending a photo, picture or video.')
reports_created = _('Your message has been sent to the Bot\'s developer. He will fix the problem soon '
                    'and you will receive a notification.\n'
                    'Thanks for your feedback!')

error_occured = _('Looks like an error occured... The Bot\'s developer already working on it...')
