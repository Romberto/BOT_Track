from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.workers.googletab import SheetDoc
from keyboard import no_pay_kb, kb_start
from loader import dp
from states.new_track_state import NewTrackState
from states.no_pay_states import NoPayState

ss = SheetDoc()


@dp.callback_query_handler(state=NoPayState.start)
async def get_no_pay(call: types.CallbackQuery, state=FSMContext):
    if call.data != 'other_pay':
        await state.set_state(NoPayState.change)
        data = await ss.get_row(int(call.data))
        await state.update_data(row=call.data)
        mes = f'Неоплаченная доставка {data[0]}, на сумму {int(data[2])+int(data[3])}\nпоменять статус?'
        await call.message.answer(mes, reply_markup=no_pay_kb)
    else:
        await state.set_state(NoPayState.other_pay)
        buttons = types.InlineKeyboardMarkup(row_width=2)
        buttons.add(
            types.InlineKeyboardButton(text='ДА', callback_data='yes'),
            types.InlineKeyboardButton(text='НЕТ', callback_data='no')
        )
        await call.message.answer('Пометить все как оплаченные?', reply_markup=buttons)

@dp.callback_query_handler(state=NoPayState.other_pay)
async def other_pay(call:types.CallbackQuery, state:FSMContext):
    ss = SheetDoc()
    if call.data == 'yes':
        await call.message.answer('Все доставки помеченны как оплаченны')
        data = await ss.get_track(prefix='no_pay')
        for element in data['rows']:
            key = (list(element.keys())[0])
            await ss.toggle_status(row_number=key)
        await state.finish()


    elif call.data == 'no':

        await call.message.answer('запрос получен, ждите ...')
        data = await ss.get_track(prefix='no_pay')
        if data['count'] != 0:
            button_kb = types.InlineKeyboardMarkup(row_width=1)
            await state.set_state(NoPayState.start)
            for element in data['rows']:
                key = (list(element.keys())[0])
                button_kb.add(types.InlineKeyboardButton(text=str(element[key]), callback_data=key))
            button_kb.add(types.InlineKeyboardButton(text='Пометить все как оплаченные', callback_data='other_pay'))
            await call.message.answer(f'Всего НЕОПЛАЧЕННЫХ {data["count"]}\n на сумму {data["summ"]}',
                                 reply_markup=button_kb)

@dp.message_handler(text='Пометить как оплачено', state=NoPayState.change)
async def change_status(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    number_row = state_data['row']
    await ss.toggle_status(int(number_row))
    await state.finish()
    await message.answer('статус успешно изменён',reply_markup=kb_start)


@dp.message_handler(text='Новая доставка', state=NoPayState.start)
async def new_track(message: types.Message, state: FSMContext):
    await state.finish()
    await NewTrackState.start.set()
    await message.answer('Количество машин')