from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard import kb_start
from loader import dp


@dp.message_handler(text=['/start','Меню'], state='*')
async def start(message: types.Message, state:FSMContext):
    await state.finish()
    if message.chat.id == 841163160:
        await message.answer(f'Hello', reply_markup=kb_start)
    else:
        await message.answer('Кто ты? Я с незнакомцами не разговариваю.')
