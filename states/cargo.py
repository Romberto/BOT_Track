from aiogram.dispatcher.filters.state import State, StatesGroup


class CargoState(StatesGroup):
    start = State()
    cargo = State()


class AddProductState(StatesGroup):
    start = State()
    weight = State()
    box = State()
    quantity = State()
    price = State()


class ProductState(StatesGroup):
    start = State()
    edit = State()
    edit_price = State()
    del_questions = State()


class FormingCargoState(StatesGroup):
    start = State()
    quantity = State()
    cargo_del = State()
