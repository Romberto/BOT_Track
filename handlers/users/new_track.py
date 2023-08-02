from aiogram.dispatcher import FSMContext

from handlers.workers.googletab import SheetDoc
from loader import dp
from aiogram import types

from states.new_track_state import NewTrackState


@dp.message_handler(text='Новая доставка')
async def new_track(message: types.Message, state: FSMContext):
    await NewTrackState.start.set()
    await message.answer('Количество машин')


@dp.message_handler(content_types=types.ContentType.TEXT, state=NewTrackState.start)
async def get_number_cars(message: types.Message, state: FSMContext):
    await NewTrackState.number_car.set()
    if message.text.isdigit():
        await message.answer('добавляю строку со статусом неоплачено')
        quantity_cars = int(message.text)
        summ_azs = (quantity_cars * 100)
        ss = SheetDoc()
        # todo добавить метод для добавления строки в google таблицу, метод принимае два аргумента: summ , numbers
        await ss.add_row(quantity_cars,summ_azs)
        await message.answer(f'строка добавленна')

        await state.finish()
    else:
        await message.answer('сумма принимается только цифрами')



