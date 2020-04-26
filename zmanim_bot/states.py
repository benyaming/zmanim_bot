from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.redis import RedisStorage2


class GregorianDate(StatesGroup):
    waiting_for_gregorian_date = State()


class HebrewDate(StatesGroup):
    waiting_for_hebrew_date = State()


class Feedback(StatesGroup):
    waiting_for_feedback_text = State()
