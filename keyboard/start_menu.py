from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_start = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Все доставки'),
            KeyboardButton(text='Оплаченные'),
            KeyboardButton(text='Неоплаченные')],
        [
            KeyboardButton(text='Новая доставка')
        ],
    ], resize_keyboard=True, one_time_keyboard=True, row_width=3)
