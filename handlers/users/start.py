from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard import kb_start
from loader import dp


@dp.message_handler(text='/start', state='*')
async def start(message: types.Message, state:FSMContext):
    await state.finish()
    await message.answer('Hello', reply_markup=kb_start)
