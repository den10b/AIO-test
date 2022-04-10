import asyncio
import logging
import os.path
from typing import Any
import random

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
    name = State()
    grade = State()
    choose_grade = State()
    menu = State()
    ask = State()
    finalQuest = State()
    finalInf = State()


async def get_data(dialog_manager: DialogManager, **kwargs):
    return {
        'id': dialog_manager.current_context().dialog_data.get("id", None),
        'name': dialog_manager.current_context().dialog_data.get("name", None),
        'grade': dialog_manager.current_context().dialog_data.get("grade", None),
    }


async def start(m: Message, dialog_manager: DialogManager):
    if not (await ActiveUsers.filter(user_id=m.from_user.id).values_list("user_id")):
        await dialog_manager.start(UserSG.hi, mode=StartMode.RESET_STACK)
        # Если его нет в базе, то предлагаем зарегистрироваться
        dialog_manager.current_context().dialog_data["id"] = m.from_user.id
    else:
        await dialog_manager.start(UserSG.menu, mode=StartMode.RESET_STACK)
        # Если он есть то переходим в меню
        dialog_manager.current_context().dialog_data["name"] = \
            (await ActiveUsers.filter(user_id=m.from_user.id).values_list("user_name"))[0]
        dialog_manager.current_context().dialog_data["grade"] = \
            (await ActiveUsers.filter(user_id=m.from_user.id).values_list("grade"))[0]
        dialog_manager.current_context().dialog_data["id"] = m.from_user.id


async def quest_handler(m: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager):
    count = Counter.get_count()
    name = (await ActiveUsers.filter(user_id=m.from_user.id).values_list("code_name", flat=True))[0]
    while await Questions.filter(key=count).values_list():
        count = Counter.get_count()  # Присваиваем вопросу идентификатор
    await bot.send_message(CHAT_ID, f'<b>{str(count)}</b>' + '\n' + m.text + "\nОт: " + name, parse_mode="HTML")
    await Questions(key=count, user_id_id=m.from_user.id, question=m.text, is_answered=False).save()
    await manager.dialog().switch_to(UserSG.finalQuest)


async def name_handler(m: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager):
    manager.current_context().dialog_data["name"] = m.text
    await manager.dialog().switch_to(UserSG.grade)


async def on_student_clicked(c: CallbackQuery, button: Button, manager: DialogManager):
    count = NameCounter.get_count()
    manager.current_context().dialog_data["grade"] = "12"
    while await ActiveUsers.filter(code_name=count).values_list():
        count = NameCounter.get_count()
    await ActiveUsers(user_id=manager.current_context().dialog_data["id"],
                      code_name=count,
                      user_name=manager.current_context().dialog_data["name"],
                      grade="12"
                      ).save()
    await bot.send_message(manager.current_context().dialog_data["id"], "Поздравляю, вы зареганы!")
    await manager.dialog().switch_to(UserSG.menu)


async def on_grade_clicked(c: ChatEvent, select: Select, manager: DialogManager, item_id: str):
    count = NameCounter.get_count()
    manager.current_context().dialog_data["grade"] = item_id
    while await ActiveUsers.filter(code_name=count).values_list():
        count = NameCounter.get_count()
    await ActiveUsers(user_id=manager.current_context().dialog_data["id"],
                      code_name=count,
                      user_name=manager.current_context().dialog_data["name"],
                      grade=manager.current_context().dialog_data["grade"]
                      ).save()
    await bot.send_message(manager.current_context().dialog_data["id"], "Поздравляю, вы зареганы!")
    await manager.dialog().switch_to(UserSG.menu)


async def on_inf_clicked(c: CallbackQuery, button: Button, manager: DialogManager):
    if manager.current_context().dialog_data["grade"] != 12:
        await bot.send_message(manager.current_context().dialog_data["id"], "Информация для школьников")
    else:
        await bot.send_message(manager.current_context().dialog_data["id"], "Информация для студентов")
    await manager.dialog().switch_to(UserSG.finalInf)


usr_dialog = Dialog(
    Window(
        Const("Greetings! Мы - КРОК, пройди пжж регистрацию"),
        SwitchTo(Const("Зарегистрироваться!"), id="fi", state=UserSG.name),
        Back(Const("⏪ Назад в утробу")),
        state=UserSG.hi
    ),
    Window(
        Const("Как тебя зовут?"),
        MessageInput(name_handler),
        Back(Const("⏪ Назад")),
        state=UserSG.name
    ),
    Window(
        Const("Ты школьник или студент?"),
        SwitchTo(Const("Школьник"), id="school", state=UserSG.choose_grade),
        Button(Const("Студент"), id="student", on_click=on_student_clicked),
        Back(Const("⏪ Назад")),
        state=UserSG.grade
    ),
    Window(
        Const("В каком ты классе?"),
        Back(Const("⏪ Назад")),
        Row(Select(
            Format("{item}"),
            items=["<7",
                   "8",
                   "9",
                   "10",
                   "11"
                   ],
            item_id_getter=lambda x: x,
            id="grades",
            on_click=on_grade_clicked,
        )),
        state=UserSG.choose_grade
    ),
    Window(
        Format("{name}, что тебя интересует?"),
        SwitchTo(Const("Задать вопрос ❓"), id="qu", state=UserSG.ask),
        Button(Const("Посмотреть инф. о программах для меня"), id="qu2", on_click=on_inf_clicked),
        # Сюда кнопки меню
        getter=get_data,
        state=UserSG.menu
    ),
    Window(
        Const("Введите вопрос"),
        MessageInput(quest_handler),
        Back(Const("⏪ Назад")),
        state=UserSG.ask
    ),
    Window(
        Const('Вопрос отправлен!'),
        state=UserSG.finalQuest
    ),
    Window(
        Const('Вот подходящая информация!'),
        state=UserSG.finalInf
    )
)
