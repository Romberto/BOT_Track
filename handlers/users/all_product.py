from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.workers.cargoman import Cargonist
from keyboard.cargo_kb import product_kb
from loader import dp
from states.cargo import CargoState, ProductState


@dp.message_handler(state=[CargoState.start, ProductState.edit, ProductState.start], text=['Продукты','все продукты'])
async def all_product(message: types.Message, state=FSMContext):
    await state.set_state(ProductState.start)
    cargo = Cargonist()
    all_product = await cargo.get_all_product()
    buttons = types.InlineKeyboardMarkup(row_width=1)

    for item in all_product:
        buttons.add(types.InlineKeyboardButton(text=item[0], callback_data=item[0]))
    await message.answer('Выберите продукт', reply_markup=buttons)


@dp.callback_query_handler(state=ProductState.start)
async def product(call: types.CallbackQuery, state: FSMContext):
    cargo = Cargonist()
    product = await cargo.get_by_name(call.data)
    await state.set_state(ProductState.edit)
    await state.update_data(product=product)
    await call.message.answer(
        f'{product.name}\nна поддоне {product.boxs} коробок;\nв коробке {product.quantity} бут/кг\nвес единицы {product.weight} кг.\nцена: {product.price} руб.',
        reply_markup=product_kb)




@dp.message_handler(state=ProductState.edit, text='Удалить')
async def del_product_question(message: types.Message, state: FSMContext):
    await state.set_state(ProductState.del_questions)
    data = await state.get_data()
    product = data['product']
    buttons = types.InlineKeyboardMarkup(row_width=2)
    buttons.add(
        types.InlineKeyboardButton(text='ДА', callback_data='yes'),
        types.InlineKeyboardButton(text='НЕТ', callback_data='no')
    )
    await message.answer(f'Удалить {product.name} ?', reply_markup=buttons)


@dp.callback_query_handler(state=ProductState.del_questions)
async def del_product(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        await state.set_state(ProductState.start)
        cargo = Cargonist()
        data = await state.get_data()
        product = data['product']
        await cargo.delete_product(product.name)
        all_product = await cargo.get_all_product()
        buttons = types.InlineKeyboardMarkup(row_width=1)
        for item in all_product:
            buttons.add(types.InlineKeyboardButton(text=item[0], callback_data=item[0]))
        await call.message.answer('Выберите продукт', reply_markup=buttons)

    elif call.data == 'no':
        await state.set_state(ProductState.start)
        cargo = Cargonist()
        all_product = await cargo.get_all_product()
        buttons = types.InlineKeyboardMarkup(row_width=1)
        for item in all_product:
            buttons.add(types.InlineKeyboardButton(text=item[0], callback_data=item[0]))
        await call.message.answer('Выберите продукт', reply_markup=buttons)

@dp.message_handler(state=ProductState.edit, text='Изменить цену')
async def del_product_question(message: types.Message, state: FSMContext):
    await state.set_state(ProductState.edit_price)
    data = await state.get_data()
    product = data['product']
    await message.answer(f'Укажите новую цену для продукта {product.name}')

@dp.message_handler(state=ProductState.edit_price, content_types=types.ContentType.TEXT)
async def edit_price(message:types.Message, state:FSMContext):
    if message.text.isalpha():
        await message.answer('Укажите цену цифрами')
    else:
        data = await state.get_data()
        product = data['product']
        cargo = Cargonist()
        try:
            await state.set_state(ProductState.edit)
            await cargo.edit_price(product.name, float(message.text))

            await message.answer(f'Цена на {product.name} успешно изменина')
        except Exception as er:
            await message.answer(f'ОШИБКА !!! {er}')







