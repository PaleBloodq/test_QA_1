from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start, Url, Back, Next, Button
from aiogram_dialog.widgets.text import Const, Format

from .handlers import process_no_ps4, process_no_ps5, process_yes, process_no
from .methods import getter_order, resending
from states.states import OrderSG, MainSG, TwoFaSG
from ...custom_widgets import ScrollingOrdersGroup
from ...filters import is_can_pay, is_can_send_message, is_paid

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
        Url(Const('Оплатить'), id='pay', url=Format('{order.payment_url}'), when=is_can_pay),
        #Next(Const('💬Написать менеджеру'), id='next', when=is_can_send_message),
        # Start(Const('🔒Как включить 2FA?'), state=TwoFaSG.show, id='2FA'),
        #Back(Const('Назад')),
        Button(Const('Да'), id='test_yes', on_click=process_yes, when=is_paid, ),
        Button(Const('Нет'), id='test_no', on_click=process_no, when=is_paid),
        parse_mode='MarkdownV2',
        getter=getter_order,
        state=OrderSG.order,
    ),
    Window(
        Const('Выполните это, это и то'),
        Button(Const('ps 4'), id='ps4', on_click=process_no_ps4),
        Button(Const('ps 5'), id='ps5', on_click=process_no_ps5),
        Back(Const('Назад')),
        state=OrderSG.no_options,
    ),
    Window(
        Const('Текст для ps 4'),
        Button(Const('ps 5'), id='ps5', on_click=process_no_ps5),
        Button(Const('Подключено'), id='connected', on_click=process_yes),
        Back(Const('Назад')),
        state=OrderSG.ps4,
    ),
    Window(
        Const('Текст для ps 5'),
        Button(Const('ps 4'), id='ps4', on_click=process_no_ps4),
        Button(Const('Подключено'), id='connected', on_click=process_yes),
        Back(Const('Назад')),
        state=OrderSG.ps5,
    ),
    Window(
        Const('Отправьте сообщение'),
        MessageInput(func=resending),
        Back(Const('Назад')),
        state=OrderSG.input_answer,
    ),
]

