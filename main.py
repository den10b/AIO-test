import asyncio
import logging
import os.path
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ContentType

from aiogram_dialog import Dialog, DialogManager, DialogRegistry, Window, ChatEvent, StartMode
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select, Row, SwitchTo, Back
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

src_dir = os.path.normpath(os.path.join(__file__, os.path.pardir))

API_TOKEN = "5176288897:AAFWal8jXz6Z4SKPJYf4MNsxc5tRskDQRYY"
CHAT_ID = "-721759162"
DATA = []
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


class DialogSG(StatesGroup):
    hi = State()
    admin = State()
    ask = State()


async def qest_handler(m: Message, dialog: ManagedDialogAdapterProto,
                       manager: DialogManager):
    x = await bot.send_message(CHAT_ID, m.text)
    DATA.append(x.message_id)


async def answ_handler(m: Message, dialog: ManagedDialogAdapterProto,
                       manager: DialogManager):
    await Bot(token=API_TOKEN).send_message(CHAT_ID, m.text)


dialog = Dialog(
    Window(
        Const("Greetings!"),
        SwitchTo(Const("I hawe Qetstion"), id="fi", state=DialogSG.ask),
        state=DialogSG.hi
    ),
    Window(
        Const("Ask:"),
        MessageInput(qest_handler),
        state=DialogSG.ask
    ),
    Window(
        Const("Greetings! Please, ask:"),
        MessageInput(answ_handler),
        state=DialogSG.admin
    )
)


async def start(m: Message, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(DialogSG.hi, mode=StartMode.RESET_STACK)


async def admin(m: Message, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(DialogSG.admin, mode=StartMode.RESET_STACK)


async def main():
    dp.register_message_handler(start, text="/start", state="*")
    dp.register_message_handler(start, text="/admin", state="*")
    registry = DialogRegistry(dp)
    registry.register(dialog)

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
