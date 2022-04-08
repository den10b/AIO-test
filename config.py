import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import random

API_TOKEN = "5176288897:AAFWal8jXz6Z4SKPJYf4MNsxc5tRskDQRYY"
CHAT_ID = "-721759162"
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
stuff = [
    "red", "blue", "green", "brown", "yellow", "white"
]


# def get_code_name():
#     return str("#"+random.choice(stuff) + str(random.randint(11, 99)))


class NameCounter:
    TOKEN = 10

    @classmethod
    def get_count(cls):
        Counter.TOKEN = Counter.TOKEN + 1
        return str("#" + random.choice(stuff)) + cls.TOKEN.__str__()


class Counter:
    TOKEN = 110

    @classmethod
    def get_count(cls):
        Counter.TOKEN = Counter.TOKEN + 1
        return "#" + cls.TOKEN.__str__()
