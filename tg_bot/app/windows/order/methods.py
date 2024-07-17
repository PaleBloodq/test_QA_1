import asyncio
import base64
import itertools
import re

from aiogram.types import Message
from aiogram_dialog import DialogManager

import bootstrap
from app.windows.order.handlers import answer_order, bot
from service.managers.user_data_manager import UserData


async def getter_order(dialog_manager: DialogManager, **kwargs):
    order = UserData(dialog_manager).data.selected_order
    order_extra = order.get_order_extra()
    return {'order': order,
            'order_extra': order_extra,
            'order_products': order.get_normalized_products()}


async def resending(message: Message, __, manager: DialogManager):
    # await answer_order(message, manager)
    regex = r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
    match = re.search(regex, message)
    order_id = match.group(1)
    image_bs64 = None
    text = message.text or message.caption
    if not text:
        await message.reply('Ответ не может быть без текста')
        return
    if order_id:
        if message.photo:
            image = message.photo[-1].file_id
            import io
            image_io = io.BytesIO()
            await bot.download(image, destination=image_io)
            image_bs64 = base64.b64encode(image_io.getvalue()).decode('utf-8')
        await bootstrap.ApiWrapper.send_message(order_id=order_id, text=text, image=image_bs64)
        print(order_id)
        await message.reply('Отлично! Ответ отправлен')

async def delete_timer(message: Message):
    spinner = itertools.cycle(['◴', '◷', '◶', '◵'])
    for i in range(4):
        await asyncio.sleep(1)
        await message.edit_text(text=message.text + f' {next(spinner)}')
    await message.delete()
