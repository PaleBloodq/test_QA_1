from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import WebApp, Button, Start, Url, Back, Next
from aiogram_dialog.widgets.text import Const, Format

from .methods import getter_order, view_id, resending
from states.states import OrderSG, MainSG, TwoFaSG
from ...custom_widgets import ScrollingOrdersGroup
from ...filters import is_can_pay, is_can_send_message

OrderWin = [
    Window(
        Const('📦Ваши заказы'),
        ScrollingOrdersGroup(),
        Start(Const('Назад'), state=MainSG.main_menu, id='back'),
        state=OrderSG.order_list,
    ),
    Window(
        Format('📦Заказ от *{order.date}*'),
        Format('ℹ️Статус заказа: *{order_extra.status_text} {order_extra.emoji}*'),
        Format('💰Общая стоимость: *{order.amount}₽*'),
        Format('🛒Состав заказа: \n{order_products}'),
        Format('_{order_extra.text}_'),
        Url(Const('💳Оплатить'), id='pay', url=Format('order.payment_url'), when=is_can_pay),
        Next(Const('💬Написать менеджеру'), id='next', when=is_can_send_message),
        Start(Const('🔒Как включить 2FA?'), state=TwoFaSG.show, id='2FA'),
        Button(Const('🔎Посмотреть ID заказа'), on_click=view_id, id='order_id'),
        Back(Const('Назад')),
        parse_mode='markdown',
        getter=getter_order,
        state=OrderSG.order,
    ),
    Window(
        Const('Отправьте сообщение'),
        MessageInput(func=resending),
        Back(Const('Назад')),
        state=OrderSG.input_answer,
    ),
]
