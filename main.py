import asyncio
import logging
import os.path
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ContentType, ChatType

from aiogram_dialog import Dialog, DialogManager, DialogRegistry, Window, ChatEvent, StartMode
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select, Row, SwitchTo, Back
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

src_dir = os.path.normpath(os.path.join(__file__, os.path.pardir))

API_TOKEN = "5176288897:AAFWal8jXz6Z4SKPJYf4MNsxc5tRskDQRYY"
CHAT_ID = "-721759162"
DATA = {}
ACTIVE_USERS = []
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


class counter:
    TOKEN = 110

    @classmethod
    def get_count(cls):
        counter.TOKEN = counter.TOKEN + 1
        return cls.TOKEN


class UserSG(StatesGroup):
    hi = State()
    ask = State()
    admin = State()
    answ = State()
    post = State()


async def qest_handler(m: Message, dialog: ManagedDialogAdapterProto,
                       manager: DialogManager):
    count = counter.get_count()
    await bot.send_message(CHAT_ID, m.text + " " + str(count))
    DATA[count] = m.from_user.id


async def answ_handler(m: Message, dialog: ManagedDialogAdapterProto,
                       manager: DialogManager):
    keys = DATA.keys()
    for i in keys:
        if m.text.find(str(i)):
            await bot.send_message(DATA[i], m.text)


async def post_handler(m: Message, dialog: ManagedDialogAdapterProto,
                       manager: DialogManager):
    for usr in ACTIVE_USERS:
        await bot.send_message(usr, m.text)


dialog = Dialog(
    Window(
        Const("Greetings!"),
        SwitchTo(Const("I hawe Qetstion"), id="fi", state=UserSG.ask),
        state=UserSG.hi
    ),
    Window(
        Const("Ask:"),
        MessageInput(qest_handler),
        state=UserSG.ask
    ),
    Window(
        Const("Hello, admin"),
        SwitchTo(Const("I want to answer"), id="an", state=UserSG.answ),
        SwitchTo(Const("I want to post"), id="po", state=UserSG.post),
        state=UserSG.admin
    ),
    Window(
        Const("Please, answer:"),
        MessageInput(answ_handler),
        state=UserSG.answ
    ),
    Window(
        Const("Please, send post:"),
        MessageInput(post_handler),
        state=UserSG.post
    )
)


async def start(m: Message, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    check = True
    for usr in ACTIVE_USERS:
        if usr == m.from_user.id:
            check = False
    if check:
        ACTIVE_USERS.append(m.from_user.id)
    await dialog_manager.start(UserSG.hi, mode=StartMode.RESET_STACK)


async def admin(m: Message, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(UserSG.admin, mode=StartMode.NORMAL)


async def post(m: Message, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(UserSG.post, mode=StartMode.NORMAL)


async def main():
    dp.register_message_handler(start, text="/start", state="*")
    dp.register_message_handler(admin, text="/admin", state="*")
    registry = DialogRegistry(dp)
    registry.register(dialog)

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
