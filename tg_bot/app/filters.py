from typing import Dict
from urllib.parse import urlparse

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable

from service.managers.user_data_manager import UserData


def is_can_pay(data: Dict, widget: Whenable, manager: DialogManager):
    """Проверка на показ кнопки оплаты"""
    order = UserData(manager).data.selected_order
    parsed_url = urlparse(order.payment_url)
    return order.status == "PAYMENT" and all([parsed_url.scheme, parsed_url.netloc])


def is_can_send_message(data: Dict, widget: Whenable, manager: DialogManager):
    """Проверка на показ кнопки оплаты"""
    order = UserData(manager).data.selected_order
    return order.status not in ("ERROR", "COMPLETED")


def is_paid(data: Dict, widget: Whenable, manager: DialogManager):
    """Проверка на наличие оплаты"""
    order = UserData(manager).data.selected_order
    return order.status == "PAID"
