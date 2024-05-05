import re

from aiogram import types
from aiogram_dialog import DialogManager

import bootstrap
from states.states import MainSG


async def start(message: types.Message, dialog_manager: DialogManager | None = None):
    await dialog_manager.start(state=MainSG.main_menu)


async def answer_order(message: types.Message, dialog_manager: DialogManager | None = None):
    regex = r"№([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
    match = re.search(regex, message.reply_to_message.text)
    order_id = match.group(1)
    await bootstrap.ApiWrapper.send_message(order_id=order_id, text=message.text)
    print(order_id)
    await message.reply('Отлично! Ответ отправлен')
