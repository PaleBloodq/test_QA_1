from aiogram import types
from aiogram_dialog import DialogManager

import bootstrap
from service.managers.user_data_manager import UserData


async def send_code(message: types.Message, _, dialog_manager: DialogManager):
    data = UserData(dialog_manager).data
    await bootstrap.ApiWrapper.send_message(order_id=data.selected_order.order_id.replace('\\', ''), text=message.text)
    await message.reply('Отлично! Ответ отправлен')
    await dialog_manager.done()


async def get_help(callback: types.CallbackQuery, _, dialog_manager: DialogManager):
    data = UserData(dialog_manager).data
    await bootstrap.ApiWrapper.send_message(order_id=data.selected_order.order_id.replace('\\', ''),
                                            text="system_message:Клиенту нужна помощь в получении двухфакторки")
    await callback.message.reply('Ожидайте,скоро менеджер подключится для дальнейшей помощи.')
    await dialog_manager.done()