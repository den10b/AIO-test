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


class DialogSG(StatesGroup):
    hi = State()


async def qest_handler(m: Message, dialog: ManagedDialogAdapterProto,
                       manager: DialogManager):
    await Bot(token=API_TOKEN).send_message(CHAT_ID, m.text)


dialog = Dialog(
    Window(
        Const("Greetings! Please, ask:"),
        MessageInput(qest_handler),
        state=DialogSG.hi
    )
)


async def start(m: Message, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(DialogSG.hi, mode=StartMode.RESET_STACK)


async def main():
    # real main
    logging.basicConfig(level=logging.INFO)
    storage = MemoryStorage()
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=storage)
    dp.register_message_handler(start, text="/start", state="*")
    registry = DialogRegistry(dp)
    registry.register(dialog)

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
