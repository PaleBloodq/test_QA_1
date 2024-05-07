import logging
from urllib.parse import urlparse, parse_qs

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

import bootstrap

from service.managers.user_data_manager import UserData
from states.states import OrderSG
flatten = lambda lst: sum(([x] if not isinstance(x, list) else flatten(x) for x in lst), [])


async def getter_token(dialog_manager: DialogManager, **kwargs):
    token = UserData(dialog_manager).data.token
    logging.warning(UserData(dialog_manager).data)
    logging.warning(token)
    if token:
        return {'token': token}
    await dialog_manager.reset_stack()


async def open_orders(callback: CallbackQuery, __, manager: DialogManager):
    if not UserData(manager).data.token:
        for kbd in flatten(callback.message.reply_markup.inline_keyboard):
            if kbd.web_app:
                parsed_url = urlparse(kbd.web_app.url)
                query_params = parse_qs(parsed_url.query)
                token = query_params.get('token')[0]
                UserData(manager).data.token = token
    await manager.start(OrderSG.order_list)
