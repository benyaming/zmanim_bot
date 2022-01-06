from aiogram.types import ContentType

from zmanim_bot import exceptions as e
from zmanim_bot.admin.states import AdminReportResponse
from zmanim_bot.config import config
from zmanim_bot.helpers import CallbackPrefixes, LOCATION_PATTERN
from zmanim_bot.misc import dp
from zmanim_bot.states import FeedbackState, ConverterGregorianDateState, ConverterJewishDateState, \
    LocationNameState, ZmanimGregorianDateState
from . import admin, converter, errors, festivals, forms, main, menus, settings, \
    incorrect_text_handler, reset_handler, payments, geolocation
from ..texts.single import buttons

__all__ = ['register_handlers']


def register_handlers():
    # errors
    dp.register_errors_handler(errors.no_location_exception_handler, exception=e.NoLocationException)
    dp.register_errors_handler(errors.incorrect_location_exception_handler, exception=e.IncorrectLocationException)
    dp.register_errors_handler(errors.non_unique_location_exception_handler, exception=e.NonUniqueLocationException)
    dp.register_errors_handler(errors.non_unique_location_name_exception_handler, exception=e.NonUniqueLocationNameException)
    dp.register_errors_handler(errors.location_limit_exception_handler, exception=e.MaxLocationLimitException)
    dp.register_errors_handler(errors.no_language_exception_handler, exception=e.NoLanguageException)
    dp.register_errors_handler(errors.gregorian_date_exception_handler, exception=e.IncorrectGregorianDateException)
    dp.register_errors_handler(errors.jewish_date_exception_handler, exception=e.IncorrectJewishDateException)
    dp.register_errors_handler(errors.polar_coordinates_exception_handler, exception=e.PolarCoordinatesException)
    dp.register_errors_handler(errors.unknown_processor_exception_handler, exception=e.UnknownProcessorException)
    dp.register_errors_handler(errors.main_errors_handler, exception=Exception)

    # reset handlers whech clears any state (should be first!)
    dp.register_message_handler(reset_handler.handle_start, commands=['start'])
    dp.register_message_handler(reset_handler.handle_back, text=[buttons.back, buttons.cancel], state="*")

    # admin
    dp.register_message_handler(admin.handle_report_response, lambda msg: msg.from_user.id in config.REPORT_ADMIN_LIST, state=AdminReportResponse.waiting_for_response_text)
    dp.register_message_handler(admin.handle_done_report, text=buttons.done, state=AdminReportResponse.waiting_for_payload)
    dp.register_message_handler(admin.handle_report_payload, content_types=ContentType.ANY, state=AdminReportResponse.waiting_for_payload)
    dp.register_callback_query_handler(admin.handle_report, lambda call: call.from_user.id in config.REPORT_ADMIN_LIST, text_startswith=CallbackPrefixes.report)

    # forms/states
    dp.register_message_handler(forms.handle_report, state=FeedbackState.waiting_for_feedback_text)
    dp.register_message_handler(forms.handle_done_report, text=buttons.done, state=FeedbackState.waiting_for_payload)
    dp.register_message_handler(forms.handle_report_payload, content_types=ContentType.ANY, state=FeedbackState.waiting_for_payload)
    dp.register_message_handler(forms.handle_converter_gregorian_date, state=ConverterGregorianDateState.waiting_for_gregorian_date)
    dp.register_message_handler(forms.handle_converter_jewish_date, state=ConverterJewishDateState.waiting_for_jewish_date)
    dp.register_message_handler(forms.handle_zmanim_gregorian_date, state=ZmanimGregorianDateState.waiting_for_gregorian_date)
    dp.register_message_handler(forms.handle_location_name, state=LocationNameState.waiting_for_location_name_state)

    # main
    dp.register_message_handler(main.handle_zmanim, text=buttons.mm_zmanim)
    dp.register_message_handler(main.handle_zmanim_by_date, text=buttons.mm_zmanim_by_date)
    dp.register_message_handler(main.handle_shabbat, text=buttons.mm_shabbat)
    dp.register_message_handler(main.handle_daf_yomi, text=buttons.mm_daf_yomi)
    dp.register_message_handler(main.handle_rosh_chodesh, text=buttons.mm_rh)

    dp.register_callback_query_handler(main.handle_zmanim_by_date_callback, text_startswith=CallbackPrefixes.zmanim_by_date)
    dp.register_callback_query_handler(main.handle_update_zmanim, text_startswith=CallbackPrefixes.update_zmanim)
    dp.register_callback_query_handler(main.handle_update_shabbat, text_startswith=CallbackPrefixes.update_shabbat)

    # menus
    dp.register_message_handler(menus.handle_holidays_menu, text=[buttons.mm_holidays, buttons.hom_main])
    dp.register_message_handler(menus.handle_more_holidays_menu, text=buttons.hom_more)
    dp.register_message_handler(menus.handle_fasts_menu, text=buttons.mm_fasts)
    dp.register_message_handler(menus.handle_settings_menu, commands=['settings'])
    dp.register_message_handler(menus.handle_settings_menu, text=buttons.mm_settings)
    dp.register_message_handler(menus.handle_donate, text=buttons.mm_donate)

    # festivals
    dp.register_message_handler(festivals.handle_fast, text=buttons.FASTS)
    dp.register_message_handler(festivals.handle_yom_tov, text=buttons.YOMTOVS)
    dp.register_message_handler(festivals.handle_holiday, text=buttons.HOLIDAYS)

    dp.register_callback_query_handler(festivals.handle_fast_update, text_startswith=CallbackPrefixes.update_fast)
    dp.register_callback_query_handler(festivals.handle_yom_tov_update, text_startswith=CallbackPrefixes.update_yom_tov)

    # converter
    dp.register_message_handler(converter.handle_converter_entry, commands=['converter_api'])
    dp.register_message_handler(converter.handle_converter_entry, text=buttons.mm_converter)
    dp.register_message_handler(converter.start_greg_to_jew_converter, text=buttons.conv_greg_to_jew)
    dp.register_message_handler(converter.start_jew_to_greg_converter, text=buttons.conv_jew_to_greg)

    # settings
    dp.register_message_handler(settings.settings_menu_cl, text=buttons.sm_candle)
    dp.register_message_handler(settings.settings_menu_havdala, text=buttons.sm_havdala)
    dp.register_message_handler(settings.settings_menu_zmanim, text=buttons.sm_zmanim)
    dp.register_message_handler(settings.handle_omer_settings, text=buttons.sm_omer)
    dp.register_message_handler(settings.handle_language_request, commands=['language'])
    dp.register_message_handler(settings.handle_language_request, text=buttons.sm_lang)
    dp.register_message_handler(settings.set_language, text=config.LANGUAGE_LIST)
    dp.register_message_handler(settings.help_menu_report, commands=['report'])
    dp.register_message_handler(settings.help_menu_report, text=buttons.hm_report)

    dp.register_callback_query_handler(settings.set_cl, text_startswith=CallbackPrefixes.cl)
    dp.register_callback_query_handler(settings.set_havdala, text_startswith=CallbackPrefixes.havdala)
    dp.register_callback_query_handler(settings.set_zmanim, text_startswith=CallbackPrefixes.zmanim)
    dp.register_callback_query_handler(settings.set_omer, text_startswith=CallbackPrefixes.omer)

    # location
    dp.register_message_handler(geolocation.location_settings, commands=['location'])
    dp.register_message_handler(geolocation.location_settings, text=buttons.sm_location)
    dp.register_message_handler(geolocation.handle_location, regexp=LOCATION_PATTERN)
    dp.register_message_handler(geolocation.handle_location, content_types=[ContentType.LOCATION, ContentType.VENUE])

    dp.register_callback_query_handler(geolocation.add_new_location, text_startswith=CallbackPrefixes.location_add)
    dp.register_callback_query_handler(geolocation.manage_saved_locations, text_startswith=CallbackPrefixes.location_namage)
    dp.register_callback_query_handler(geolocation.back_to_location_settings, text_startswith=CallbackPrefixes.location_menu_back)
    dp.register_callback_query_handler(geolocation.handle_activate_location, text_startswith=CallbackPrefixes.location_activate)
    dp.register_callback_query_handler(geolocation.init_location_rename, text_startswith=CallbackPrefixes.location_rename)
    dp.register_callback_query_handler(geolocation.handle_delete_location, text_startswith=CallbackPrefixes.location_delete)

    dp.register_inline_handler(geolocation.handle_inline_location_query)

    # payments
    dp.register_callback_query_handler(payments.handle_donate, text_startswith=CallbackPrefixes.donate)
    dp.register_pre_checkout_query_handler(payments.handle_pre_checkout)
    dp.register_message_handler(payments.on_success_payment, content_types=[ContentType.SUCCESSFUL_PAYMENT])
    dp.register_message_handler(payments.on_success_payment, content_types=[ContentType])

    # unknown messages (SHOULD BE LAST!)
    dp.register_message_handler(incorrect_text_handler.handle_incorrect_text)
