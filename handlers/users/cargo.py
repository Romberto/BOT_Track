from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard import cargo_kb
from loader import dp
from states.cargo import CargoState


@dp.message_handler(text='Погрузка', state='*')
async def cargo_in(message: types.Message, state: FSMContext):
    await state.set_state(CargoState.start)
    await message.answer('Расчёт заявки на погрузку в Казахстан', reply_markup=cargo_kb)



