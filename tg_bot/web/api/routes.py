import logging
import os

import asyncio
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto,
    URLInputFile,
    InputMediaDocument,
)
from aiogram_dialog import StartMode, ShowMode
from pydantic import ValidationError

import bootstrap
from aiohttp import ClientSession
from aiohttp.abc import Request
from aiohttp.web_response import Response

from service.managers.user_data_manager import UserData
from states.states import OrderSG
from utils import create_bg_manager, escape_markdown

from .models import NewMessage, Order, Mailing


BACKEND_URL = f'{os.environ.get("BACKEND_SCHEMA")}://{os.environ.get("BACKEND_HOST")}:{os.environ.get("BACKEND_PORT")}'


bot = bootstrap.MyBot().getInstance()


async def send_message_manager(request: Request) -> Response:
    data = await request.json()
    try:
        data = NewMessage(**data)
        order_id = escape_markdown(data.order_id)
        text = f"*Сообщение от менеджера по вашему заказу ||{order_id}|| :*\n```📨 " + escape_markdown(data.text).replace('\\n', '\n')
        text += '```\n\n_Чтобы ответить на сообщение, потяните его влево, если вы с телефона, напишите текст и отправьте\n' \
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


async def mailing(request: Request) -> Response:
    data = await request.json()
    logging.warning(data)
    logging.warning(Mailing(**data))
    asyncio.create_task(send_mailing_messages(Mailing(**data)))
    return Response(status=201)


async def send_mailing_messages(mailing: Mailing):
    await asyncio.sleep(1)
    media = []
    total_messages = ()
    for url in mailing.media:
        filepath = BACKEND_URL + url
        match url.split('.')[-1]:
            case 'png' | 'jpg' | 'jpeg' | 'jfif' | 'afif' | 'gif' | 'webp' | 'heif' | 'bmp' | 'svg':
                media.append(InputMediaPhoto(media=URLInputFile(filepath)))
            case _:
                media.append(InputMediaDocument(media=URLInputFile(filepath)))
    for telegram_id in mailing.telegram_ids:
        try:
            if media:
                if len(media) == 1:
                    message = await bot.send_photo(telegram_id, media[0].media, caption=mailing.text[:1024])
                else:
                    media[0].caption = mailing.text[:1024]
                    message = await bot.send_media_group(telegram_id, media)
            else:
                message = await bot.send_message(telegram_id, mailing.text[:4096])
        except:
            continue
        total_messages += (message.message_id, )
        await asyncio.sleep(0.04)
    async with ClientSession() as session:
        await session.patch(
            BACKEND_URL + '/api/mailing/',
            json={
                'id': mailing.id,
                'messages_ids': list(total_messages),
                'received_count': len(total_messages),
                'status': 'COMPLETED',
            }
        )
