from aiogram import types
from aiogram import Dispatcher


async def set_bot_commands(dp:Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'запустить бот'),
    ])