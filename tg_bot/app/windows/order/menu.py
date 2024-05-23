from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start, Url, Back, Next
from aiogram_dialog.widgets.text import Const, Format

from .methods import getter_order, resending
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
        Format('🆔Идентификатор заказа: ||{order.order_id}||'),
        Format('💰Общая стоимость: *{order.amount}₽*'),
        Format('🛒Состав заказа: \n{order_products}'),
        Format('_{order_extra.text}_'),
        Url(Const('💳Оплатить'), id='pay', url=Format('{order.payment_url}'), when=is_can_pay),
        Next(Const('💬Написать менеджеру'), id='next', when=is_can_send_message),
        Start(Const('🔒Как включить 2FA?'), state=TwoFaSG.show, id='2FA'),
        Back(Const('Назад')),
        parse_mode='MarkdownV2',
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
