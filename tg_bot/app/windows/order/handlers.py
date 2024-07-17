import base64
import io
import re

from aiogram import types
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

import bootstrap
from service.managers.user_data_manager import UserData
from states.states import MainSG, OrderSG

bot = bootstrap.MyBot().getInstance()


async def start(message: types.Message, dialog_manager: DialogManager | None = None):
    await dialog_manager.start(state=MainSG.main_menu)


async def show_id(callback: types.CallbackQuery, dialog_manager: DialogManager | None = None):
    await callback.answer(text=f"Идентификатор заказа: {callback.data.split('_')[-1]} ", show_alert=True)


async def answer_order(message: types.Message, user_message: str, dialog_manager: DialogManager | None = None):
    order_id = UserData(dialog_manager).data.selected_order.order_id
    print(order_id)
    order_id = order_id.replace("\\", "")
    print(order_id)
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
        await bootstrap.ApiWrapper.send_message(order_id=order_id, text=f"{user_message}: {text}", image=image_bs64)
        await message.reply('Отлично! Ответ отправлен')


async def complite_2fa(call: types.CallbackQuery, __, dialog_manager: DialogManager | None = None):
    await dialog_manager.switch_to(OrderSG.success)


async def uncomplite_2fa(call: types.CallbackQuery, __, dialog_manager: DialogManager | None = None):
    await dialog_manager.switch_to(OrderSG.failed)


async def send_code(message: types.Message, __, dialog_manager: DialogManager | None = None):
    await answer_order(message=message, user_message='Код', dialog_manager=dialog_manager)
    await dialog_manager.done()


async def send_problem(message: types.Message, __, dialog_manager: DialogManager | None = None):
    await answer_order(message=message, user_message='Код', dialog_manager=dialog_manager)
    await dialog_manager.done()
