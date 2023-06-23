from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.workers.cargoman import Manager
from keyboard import kb_start
from loader import dp
from states.cargo import FormingCargoState


@dp.message_handler(state=FormingCargoState.cargo_del, text='Текстовый отчёт')
async def cargo_text(message: types.Message, state: FSMContext):
    await state.finish()
    manager = Manager()
    mes = await manager.forming_text()
    await message.answer(mes, reply_markup=kb_start)
