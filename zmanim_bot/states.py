from aiogram.dispatcher.filters.state import State, StatesGroup


class GregorianDateState(StatesGroup):
    waiting_for_gregorian_date = State()


class JewishDateState(StatesGroup):
    waiting_for_jewish_date = State()


class FeedbackState(StatesGroup):
    waiting_for_feedback_text = State()
