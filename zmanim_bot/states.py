from aiogram.dispatcher.filters.state import State, StatesGroup


class ConverterGregorianDateState(StatesGroup):
    waiting_for_gregorian_date = State()


class ConverterJewishDateState(StatesGroup):
    waiting_for_jewish_date = State()


class ZmanimGregorianDateState(StatesGroup):
    waiting_for_gregorian_date = State()


class FeedbackState(StatesGroup):
    waiting_for_feedback_text = State()
    waiting_for_payload = State()


class LocationNameState(StatesGroup):
    waiting_for_location_name_state = State()
