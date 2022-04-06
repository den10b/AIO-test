import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


API_TOKEN = "5176288897:AAFWal8jXz6Z4SKPJYf4MNsxc5tRskDQRYY"
CHAT_ID = "-721759162"
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


class counter:
    TOKEN = 110

    @classmethod
    def get_count(cls):
        counter.TOKEN = counter.TOKEN + 1
        return "#" + cls.TOKEN.__str__()
