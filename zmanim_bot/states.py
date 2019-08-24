from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    Menus = State()
    GregToHeb = State()
    HebToGreg = State()
    Zmanim = State()