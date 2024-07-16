import base64
import io
import re

from aiogram import types
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

import bootstrap
from states.states import MainSG, OrderSG

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
    image_bs64 = None
    text = message.text or message.caption
    if not text:
        await message.reply('Ответ не может быть без текста')
        return
    if order_id:
        if message.photo:
            image = message.photo[-1].file_id
            image_io = io.BytesIO()
            await bot.download(image, destination=image_io)
            image_bs64 = base64.b64encode(image_io.getvalue()).decode('utf-8')
        await bootstrap.ApiWrapper.send_message(order_id=order_id, text=text, image=image_bs64)
        print(order_id)
        await message.reply('Отлично! Ответ отправлен')


async def process_yes(c: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await c.answer("Вы нажали Да")
    await dialog_manager.done()

