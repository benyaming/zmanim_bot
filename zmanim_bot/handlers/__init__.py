from aiogram.types import ContentType

from zmanim_bot import exceptions as e
from zmanim_bot.misc import dp
from . import admin, converter, errors, festivals, forms, main, menus, settings
from . import incorrect_text_handler  # ----- SHOULD BE IMPORTED LAST
from . import reset_handler  # ----- SHOULD BE IMPORTED FIRST

__all__ = ['register_handlers']

from ..admin.states import AdminReportResponse

from ..config import REPORT_ADMIN_LIST
from ..helpers import CallbackPrefixes
from ..states import FeedbackState, ConverterGregorianDateState, ConverterJewishDateState, LocationNameState

from ..texts.single import buttons


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
    dp.register_errors_handler(errors.main_errors_handler, exception=Exception)

    # reset handlers whech clears any state (should be first!)
    dp.register_message_handler(reset_handler.handle_start, commands=['start'])
    dp.register_message_handler(reset_handler.handle_back, text=[buttons.back, buttons.cancel], state="*")

    # admin
    dp.register_callback_query_handler(
        admin.handle_report,
        lambda call: call.from_user.id in REPORT_ADMIN_LIST,
        text_startswith=CallbackPrefixes.report
    )
    dp.register_message_handler(
        admin.handle_report_response,
        lambda msg: msg.from_user.id in REPORT_ADMIN_LIST,
        state=AdminReportResponse.waiting_for_response_text
    )
    dp.register_message_handler(admin.handle_done_report, text=buttons.done, state=AdminReportResponse.waiting_for_payload)
    dp.register_message_handler(admin.handle_report_payload, content_types=ContentType.ANY, state=AdminReportResponse.waiting_for_payload)

    # commands

    # forms/states
    dp.register_message_handler(forms.handle_report, state=FeedbackState.waiting_for_feedback_text)
    dp.register_message_handler(forms.handle_done_report, text=buttons.done, state=FeedbackState.waiting_for_payload)
    dp.register_message_handler(forms.handle_report_payload, content_types=ContentType.ANY, state=FeedbackState.waiting_for_payload)
    dp.register_message_handler(forms.handle_converter_gregorian_date, state=ConverterGregorianDateState.waiting_for_gregorian_date)
    dp.register_message_handler(forms.handle_converter_jewish_date, state=ConverterJewishDateState.waiting_for_jewish_date)
    dp.register_message_handler(forms.handle_zmanim_gregorian_date, state=LocationNameState.waiting_for_location_name_state, text=buttons.done)
    dp.register_message_handler(forms.handle_location_name, state=LocationNameState.waiting_for_location_name_state)

    # messages

    # unknown messages (SHOULD BE LAST!)
