import re

from aiogram import types
from aiogram_dialog import DialogManager

import bootstrap
from states.states import MainSG


async def start(message: types.Message, dialog_manager: DialogManager | None = None):
    await dialog_manager.start(state=MainSG.main_menu)


async def answer_order(message: types.Message, dialog_manager: DialogManager | None = None):
    regex = r"№(\d*)"
    match = re.search(regex, message.reply_to_message.text)
    order_number = match.group(1)
    await bootstrap.ApiWrapper.send_message(order_number=order_number, text=message.text)
    print(order_number)
    await message.reply('Отлично! Ответ отправлен')
