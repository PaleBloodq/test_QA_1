from typing import Dict, List, Type, Callable
from urllib.parse import urlparse

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable

from service.managers.user_data_manager import UserData


class BaseFilter:
    def __call__(self, data: Dict, widget: Whenable, manager: DialogManager):
        return self.process(data, widget, manager)

    def process(self, data: Dict, widget: Whenable, manager: DialogManager) -> bool:
        raise NotImplementedError

    def __add__(self, other):
        if isinstance(other, BaseFilter):
            return CombinedFilter([self, other])
        elif isinstance(other, CombinedFilter):
            return CombinedFilter([self] + other.filters)
        else:
            raise ValueError("Can only combine with another BaseFilter or CombinedFilter")

    def __invert__(self):
        return InvertedFilter(self)


class CombinedFilter(BaseFilter):
    def __init__(self, filters: List[BaseFilter]):
        self.filters = filters

    def process(self, data: Dict, widget: Whenable, manager: DialogManager) -> bool:
        return all(flt(data, widget, manager) for flt in self.filters)


class InvertedFilter(BaseFilter):
    def __init__(self, filter: BaseFilter):
        self.filter = filter

    def process(self, data: Dict, widget: Whenable, manager: DialogManager) -> bool:
        return not self.filter(data, widget, manager)


class IsCanPay(BaseFilter):
    """Проверка на показ кнопки оплаты"""

    @classmethod
    def process(cls, data: Dict, widget: Whenable, manager: DialogManager):
        order = UserData(manager).data.selected_order
        parsed_url = urlparse(order.payment_url)
        return order.status == "PAYMENT" and all([parsed_url.scheme, parsed_url.netloc])


class IsPaid(BaseFilter):
    """Проверка на наличие оплаты"""

    @classmethod
    def process(cls, data: Dict, widget: Whenable, manager: DialogManager):
        order = UserData(manager).data.selected_order
        return order.status == "PAID"


class OrderNeedAccount(BaseFilter):
    """Проверка на необходимость создания аккаунта менеджером для пользователя"""

    @classmethod
    def process(cls, data: Dict, widget: Whenable, manager: DialogManager):
        order = UserData(manager).data.selected_order
        return order.need_account
