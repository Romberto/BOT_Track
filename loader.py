from aiogram import Bot, Dispatcher
from data.config import BOT_TOKEN, DEV_MOD
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2



bot = Bot(token=BOT_TOKEN)
if DEV_MOD == 'devel':
    storage = MemoryStorage()
else:
    storage = RedisStorage2()
dp = Dispatcher(bot=bot, storage=storage)