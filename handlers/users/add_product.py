from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.workers.cargoman import Cargonist
from loader import dp
from states.cargo import CargoState, AddProductState, ProductState


@dp.message_handler(state=[CargoState.start, ProductState.start], text='Создать продукт')
async def add_product(message: types.Message, state=FSMContext):
    await state.set_state(AddProductState.start)
    await message.answer('наименование продукта ?')


@dp.message_handler(state=AddProductState.start, content_types=types.ContentType.TEXT)
async def get_name(message: types.Message, state=FSMContext):
    if message.text:
        await state.update_data(name=message.text)
        await state.set_state(AddProductState.box)
        await message.answer('количество коробок на поддоне?')

@dp.message_handler(state=AddProductState.box, content_types=types.ContentType.TEXT)
async def get_name(message: types.Message, state=FSMContext):
    if message.text.isdigit():
        await state.update_data(boxs=int(message.text))
        await state.set_state(AddProductState.weight)
        await message.answer('сколько весит одна бутылка, если это весовой маргарин, то отправте цифру 1 ?')

@dp.message_handler(state=AddProductState.weight)
async def weight(message:types.Message, state:FSMContext):
    await state.update_data(weight=float(message.text))
    await state.set_state(AddProductState.quantity)
    await message.answer('сколько бутылок или килограмм в коробле ?')


@dp.message_handler(state=AddProductState.quantity, content_types=types.ContentType.TEXT)
async def get_price(message: types.Message, state=FSMContext):
    if message.text.isdigit():
        await state.update_data(quantity=int(message.text))
        await state.set_state(AddProductState.price)
        await message.answer('цена за бутылку или килограмм ?')


@dp.message_handler(state=AddProductState.price, content_types=types.ContentType.TEXT)
async def get_name(message: types.Message, state=FSMContext):
    try:
        price = float(message.text)
        data = await state.get_data()
        name = data['name']
        boxs = data['boxs']
        quantity = data['quantity']
        weight=data['weight']

        cargo = Cargonist()
        result = await cargo.add_product(name,boxs,quantity,price,weight)
        await cargo.close()
        await state.set_state(CargoState.start)
        if result:
            await message.answer('товар добавлен в базу')
        else:
            await message.answer('ОШИБКА !!! товар с таким названием уже существует в методе add_product')
    except Exception as er:
        await message.answer(f'ОШИБКА !!! {er}')