import base64
import io
import re

from aiogram import types
from aiogram_dialog import DialogManager

import bootstrap
from states.states import MainSG

bot = bootstrap.MyBot().getInstance()
async def start(message: types.Message, dialog_manager: DialogManager | None = None):
    await dialog_manager.start(state=MainSG.main_menu)


async def show_id(callback: types.CallbackQuery, dialog_manager: DialogManager | None = None):
    await callback.answer(text=f"Идентификатор заказа: {callback.data.split('_')[-1]} ", show_alert=True)

async def answer_order(message: types.Message, dialog_manager: DialogManager | None = None):
    callback = message.reply_to_message.text
    regex = r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
    match = re.search(regex, callback)
    order_id = match.group(1)
    if order_id:
        if message.photo:
            image = message.photo[-1].file_id
            image_io = io.BytesIO()
            bot.download(image, destination=image_io)
            image_bs64 = base64.b64encode(image_io.getvalue()).decode('utf-8')
            await bootstrap.ApiWrapper.send_message(order_id=order_id, text=message.text, image=image_bs64)
        base64.b64encode(order_id)
        await bootstrap.ApiWrapper.send_message(order_id=order_id, text=message.text)
        print(order_id)
        await message.reply('Отлично! Ответ отправлен')
