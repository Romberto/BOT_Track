import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.workers.cargoman import Cargonist, FormingCargonist
from keyboard import cargo_kb
from keyboard.cargo_kb import cargo_edit_kb
from loader import dp
from states.cargo import CargoState, FormingCargoState


@dp.message_handler(state=[CargoState.start, FormingCargoState.start, FormingCargoState.quantity],
                    text='Посмотреть груз')
async def looking_cargo(message: types.Message, state: FSMContext):
    fc = FormingCargonist()
    all_cargo = await fc.all_cargo()
    await fc.close()
    if all_cargo:
        await state.set_state(FormingCargoState.cargo_del)
        await message.answer(all_cargo, reply_markup=cargo_edit_kb)

    else:
        await message.answer('в кузове пусто...', reply_markup=cargo_kb)


@dp.message_handler(state=FormingCargoState.cargo_del, text='Удалить погрузку')
async def del_cargo(message: types.Message, state: FSMContext):
    fc = FormingCargonist()
    await fc.del_cargo()
    await fc.close()
    await state.set_state(FormingCargoState.start)
    await message.answer('Погрузка удалена, кузов пуст', reply_markup=cargo_kb)


@dp.message_handler(
    state=[CargoState.start, FormingCargoState.start, FormingCargoState.quantity, FormingCargoState.cargo_del],
    text='Формировать груз')
async def forming_cargo(message: types.Message, state: FSMContext):
    cargo = Cargonist()
    all_prod = await cargo.get_all_product()
    await state.set_state(FormingCargoState.start)
    buttons = types.InlineKeyboardMarkup()
    for product in all_prod:
        buttons.add(types.InlineKeyboardButton(text=product[0], callback_data=product[0]))
    # todo проверить наличие прошлых погрузок, предложить продолжить или начать заново
    await message.answer('какой продукт грузим ?', reply_markup=buttons)
    await cargo.close()


@dp.callback_query_handler(state=FormingCargoState.start)
async def get_quantity_p(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(product=call.data)
    await state.set_state(FormingCargoState.quantity)
    await call.message.answer(f'{call.data} сколько поддонов грузим ?')


@dp.message_handler(state=FormingCargoState.quantity)
async def save_row_cargo(message: types.Message, state: FSMContext):
    if message.text.isdigit():

        quantity = int(message.text)
        data = await state.get_data()
        name = data['product']
        fc = FormingCargonist()
        try:
            await fc.add_cargo(name, quantity)
            all_cargo = await fc.all_cargo()
            await fc.close()
            await message.answer(all_cargo, reply_markup=cargo_kb)
        except sqlite3.IntegrityError:
            await message.answer('такой продукт уже загружен')
            cargo = Cargonist()
            all_prod = await cargo.get_all_product()
            await state.set_state(FormingCargoState.start)
            buttons = types.InlineKeyboardMarkup()
            for product in all_prod:
                buttons.add(types.InlineKeyboardButton(text=product[0], callback_data=product[0]))
            # todo проверить наличие прошлых погрузок, предложить продолжить или начать заново
            await message.answer('какой продукт грузим ?', reply_markup=buttons)
            await cargo.close()

    else:
        await message.answer('количество поддонов нужно указать цифрой')
