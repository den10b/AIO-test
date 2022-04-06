import asyncio
import logging
import os.path
from typing import Any
import aiogram
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ContentType, ChatType

from aiogram_dialog import Dialog, DialogManager, DialogRegistry, Window, ChatEvent, StartMode
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select, Row, SwitchTo, Back
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

import DB
from config import *
from user import *
from group import *


async def main():
    dp.register_message_handler(start, text="/start", state="*")
    dp.register_message_handler(admin, text="/admin", state="*")
    registry = DialogRegistry(dp)
    registry.register(usr_dialog)
    registry.register(root_admin_dialog)
    registry.register(answer_dialog)
    registry.register(post_dialog)

    loop = asyncio.get_event_loop()
    loop.create_task(DB.run())

    await dp.start_polling()


if __name__ == '__main__':

    asyncio.run(main())
