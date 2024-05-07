import asyncio
import itertools
import logging

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager

import bootstrap
from service.managers.user_data_manager import UserData


async def getter_order(dialog_manager: DialogManager, **kwargs):
    order = UserData(dialog_manager).data.selected_order
    order_extra = order.get_order_extra()
    return {'order': order, 'order_extra': order_extra, 'order_products': order.get_normalized_products()}


async def view_id(callback: CallbackQuery, __, manager: DialogManager):
    order_id = UserData(manager).data.selected_order.order_id
    await callback.answer(text=f'Идентификатор заказа: {order_id}', show_alert=True)


async def resending(message: Message, __, manager: DialogManager):
    order_id = UserData(manager).data.selected_order.order_id
    await bootstrap.ApiWrapper.send_message(order_id=order_id, text=message.text)
    await message.delete()
    message = await message.answer(text=f'Ваше сообщение отправлено менеджеру')
    asyncio.create_task(delete_timer(message))
    manager.show_mode = manager.show_mode.NO_UPDATE


async def delete_timer(message: Message):
    spinner = itertools.cycle(['◴', '◷', '◶', '◵'])
    for i in range(4):
        await asyncio.sleep(1)
        await message.edit_text(text=message.text + f' {next(spinner)}')
    await message.delete()
