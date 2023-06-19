from aiogram.dispatcher.filters.state import State, StatesGroup


class NoPayState(StatesGroup):
    start = State()
    change = State()
    other_pay = State()
