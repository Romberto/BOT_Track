from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

no_pay_kb = ReplyKeyboardMarkup([
    [KeyboardButton(text='Пометить как оплачено'),
     KeyboardButton(text='/start')]
], resize_keyboard=True)
