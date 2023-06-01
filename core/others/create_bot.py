"""Создаем экземпляр бота со всеми настройками в этом файле, для отсутствия перекрестного вызова + удобство работы"""
# che
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

# from aiogram.fsm.storage.redis import RedisStorage
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.dispatcher.storage import BaseStorage

from settings import settings

# storage = RedisStorage.from_url(settings.db.redis)
storage = MemoryStorage()
bot = Bot(settings.bots.bot_token)
dp = Dispatcher(storage=storage)
