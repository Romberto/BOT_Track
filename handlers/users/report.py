from handlers.workers.googletab import SheetDoc
from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext

from states.no_pay_states import NoPayState


@dp.message_handler(text='Все доставки')
async def all_track(message: types.Message):
    ss = SheetDoc()
    await message.answer('запрос получен, ждите ...')
    data = await ss.get_track(prefix='all')
    await message.answer(f'Всего доставок {data["count"]}\n на сумму {data["summ"]}')


@dp.message_handler(text='Оплаченные')
async def all_track(message: types.Message):
    ss = SheetDoc()
    await message.answer('запрос получен, ждите ...')
    data = await ss.get_track(prefix='pay')
    if data['count'] != 0:
        await message.answer(f'Всего ОПЛАЧЕННЫХ доставок {data["count"]}\n на сумму {data["summ"]}')
    else:
        await message.answer(f'ОПЛАЧЕННЫХ доставок не найдено')


@dp.message_handler(text='Неоплаченные')
async def all_track(message: types.Message, state=FSMContext):
    ss = SheetDoc()
    await message.answer('запрос получен, ждите ...')
    data = await ss.get_track(prefix='no_pay')
    if data['count'] != 0:
        button_kb = types.InlineKeyboardMarkup(row_width=1)
        await state.set_state(NoPayState.start)
        for element in data['rows']:
            key = (list(element.keys())[0])
            button_kb.add(types.InlineKeyboardButton(text=str(element[key]), callback_data=key))
        button_kb.add(types.InlineKeyboardButton(text='Пометить все как оплаченные', callback_data='other_pay'))
        await message.answer(f'Всего НЕОПЛАЧЕННЫХ {data["count"]}\n на сумму {data["summ"]}', reply_markup=button_kb)
    else:
        await message.answer(f'НЕОПЛАЧЕННЫХ доставок не найдено')
