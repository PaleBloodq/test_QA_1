import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_dialog import StartMode, ShowMode
from pydantic import ValidationError

import bootstrap
from aiohttp.abc import Request
from aiohttp.web_response import Response

from service.managers.user_data_manager import UserData
from states.states import OrderSG
from utils import create_bg_manager, escape_markdown

from .models import NewMessage, Order

bot = bootstrap.MyBot().getInstance()


async def send_message_manager(request: Request) -> Response:
    data = await request.json()
    try:
        data = NewMessage(**data)
        text = f"*Сообщение от менеджера по вашему заказу ||{data.order_id.replace('-', '/-')}|| :*\n```📨 " + escape_markdown(data.text)
        text += '```\n\n_Чтобы ответить на сообщение, потяните его вправо, если вы с телефона, напишите текст и отправьте\n' \
                'В ином случае нажмите правой кнопкой мыши на сообщение и нажмите "Ответить"_'
        await bot.send_message(data.user_id, text=text, parse_mode='MarkdownV2')
    except Exception as e:
        print(e)
        return Response(status=400)
    return Response()


async def change_order(request: Request) -> Response:
    data = await request.json()
    logging.warning(data)
    try:
        order = Order(**data)
    except ValidationError:
        return Response(status=400)
    UserData.get_data(order.user_id).selected_order = order
    logging.warning(order)
    manager = await create_bg_manager(order.user_id)
    await manager.start(state=OrderSG.order, data=data, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)
    return Response()
