

async def on_start_app(dp):
    print('Бот запущен')
    from utils.set_bot_commands import set_bot_commands
    await set_bot_commands(dp)

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_start_app)