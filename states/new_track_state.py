from aiogram.dispatcher.filters.state import State, StatesGroup


class NewTrackState(StatesGroup):
    start = State()
    number_car = State()