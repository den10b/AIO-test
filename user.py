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

from config import *
from DB import *


class UserSG(StatesGroup):
    hi = State()
    ask = State()
    final = State()


async def start(m: Message, dialog_manager: DialogManager):
    if not (await Active_users.filter(user_id=m.from_user.id).values_list("user_id")):
        await Active_users(user_id=m.from_user.id).save()
    await dialog_manager.start(UserSG.hi, mode=StartMode.RESET_STACK)


async def quest_handler(m: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager):
    count = counter.get_count()
    while await Questions.filter(key=count).values_list("user_id"):
        count = counter.get_count()
    await bot.send_message(CHAT_ID, f'<b>{str(count)}</b>' + '\n' + m.text, parse_mode="HTML")
    await Questions(key=count, user_id=m.from_user.id, question=m.text).save()
    await manager.dialog().switch_to(UserSG.final)


usr_dialog = Dialog(
    Window(
        Const("Greetings!"),
        SwitchTo(Const("I have Question"), id="fi", state=UserSG.ask),
        state=UserSG.hi
    ),
    Window(
        Const("Ask:"),
        MessageInput(quest_handler),
        Back(Const("⏪ Назад")),
        state=UserSG.ask
    ),
    Window(
        Const('Вопрос отправлен!'),
        state=UserSG.final
    )
)
