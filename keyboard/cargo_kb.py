from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cargo_kb =  ReplyKeyboardMarkup([
    [KeyboardButton(text='Продукты'),KeyboardButton(text='Создать продукт')],
    [KeyboardButton(text='Формировать груз'), KeyboardButton(text='Посмотреть груз')],
    [KeyboardButton(text='Меню')]
],resize_keyboard=True, one_time_keyboard=True)

product_kb = ReplyKeyboardMarkup([
    [KeyboardButton(text='Удалить'),KeyboardButton(text='Изменить цену')],
    [KeyboardButton(text='все продукты')]
], resize_keyboard=True, one_time_keyboard=True)

cargo_edit_kb = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Удалить погрузку'), KeyboardButton(text='Формировать груз')
        ],
        [
            KeyboardButton(text='Текстовый отчёт')
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)

