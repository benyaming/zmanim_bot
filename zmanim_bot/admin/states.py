from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminReportResponse(StatesGroup):
    waiting_for_response_text = State()
    waiting_for_payload = State()
