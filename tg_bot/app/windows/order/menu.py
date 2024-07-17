from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start, Url, Back, Next, Button
from aiogram_dialog.widgets.text import Const, Format

from texts import COMPITE_2FA
from .handlers import answer_order, complite_2fa, send_code, send_problem, uncomplite_2fa
from .methods import getter_order
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
        Next(Const('Далее'), id='next', when=is_paid),
        Start(Const('А че это?'), state=TwoFaSG.wtf_2fa, id='2FA', when=is_paid),

        parse_mode='MarkdownV2',
        getter=getter_order,
        state=OrderSG.order,
    ),
    Window(
        Const(COMPITE_2FA),
        Button(Const('Подключил'), id="complite_2fa", on_click=complite_2fa),
        Button(Const('У меня лапки'), id="fail_2fa", on_click=uncomplite_2fa),
        state=OrderSG.choose_step

    ),
    Window(
        Const('Окей, тогда введите свой код!)'),
        MessageInput(func=send_code),
        Back(Const('Назад')),
        state=OrderSG.success,
    ),
    Window(
        Const('Окей, тогда опишите свою проблему!)'),
        MessageInput(func=send_problem),
        Back(Const('Назад')),
        state=OrderSG.failed,
    ),
]
