from typing import Callable, Dict, Union, List, Literal, Optional, Awaitable

from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram_dialog import DialogProtocol, ShowMode, ChatEvent
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition, ManagedWidget
from aiogram_dialog.widgets.kbd import Keyboard, Group, Button
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor, ensure_event_processor

import bootstrap
from service.managers.user_data_manager import UserData
from states.states import OrderSG
from web.api.models import OrderList






OnStateChanged = Callable[
    [ChatEvent, "ManagedScrollingGroupAdapter", DialogManager],
    Awaitable,
]


class ScrollingOrdersGroup(Group):
    def __init__(
            self,
            id='ORDER_SELECTOR',
            width: int = 0,
            height: Optional[int] = 5,
            when: WhenCondition = None,
            on_page_changed: Union[
                OnStateChanged, WidgetEventProcessor, None,
            ] = None,
    ):
        super().__init__(*(), id=id, width=width, when=when)
        self.height = height
        self.on_page_changed = ensure_event_processor(on_page_changed)
        self.hide_on_single_page = True
        self.orders = OrderList

    async def _render_keyboard(
            self,
            data: Dict,
            manager: DialogManager,
    ) -> List[List[InlineKeyboardButton]]:
        user_data = UserData(manager)
        response = await bootstrap.ApiWrapper.get_orders(token=user_data.data.token)
        kbd = []

        if response:
            self.orders = OrderList(**{'orders': response})
            kbd.extend([[InlineKeyboardButton(text=str(order.date.replace('\\', '')) + order.get_order_extra().emoji,
                                              callback_data=order.order_id)] for order in self.orders.orders])
        else:
            return [[InlineKeyboardButton(text='Заказов пока нет', callback_data='empty')]]


        pages = len(kbd) // self.height + bool(len(kbd) % self.height)
        last_page = pages - 1
        if pages == 0 or (pages == 1 and self.hide_on_single_page):
            return kbd
        current_page = min(last_page, self.get_page(manager))
        next_page = min(last_page, current_page + 1)
        prev_page = max(0, current_page - 1)
        pager = [
            [
                InlineKeyboardButton(
                    text="1", callback_data=self._item_callback_data("0"),
                ),
                InlineKeyboardButton(
                    text="<",
                    callback_data=self._item_callback_data(prev_page),
                ),
                InlineKeyboardButton(
                    text=str(current_page + 1),
                    callback_data=self._item_callback_data(current_page),
                ),
                InlineKeyboardButton(
                    text=">",
                    callback_data=self._item_callback_data(next_page),
                ),
                InlineKeyboardButton(
                    text=str(last_page + 1),
                    callback_data=self._item_callback_data(last_page),
                ),
            ],
        ]
        page_offset = current_page * self.height
        return kbd[page_offset: page_offset + self.height] + pager

    async def process_callback(self, callback: CallbackQuery, dialog: DialogProtocol,
                               manager: DialogManager) -> bool:
        orders = {quest.order_id: quest for quest in self.orders.orders}
        order = orders.get(callback.data)
        if callback.data.startswith(f"{self.widget_id}"):
            await self.set_page(callback, int(callback.data.split(":")[1]), manager)
            return True
        elif callback.data in orders:
            UserData(manager).data.selected_order = order
            await manager.start(OrderSG.order)
            return True
        else:
            return False

    def get_page(self, manager: DialogManager) -> int:
        return manager.current_context().widget_data.get(self.widget_id, 0)

    async def set_page(
            self, event: ChatEvent, page: int, manager: DialogManager,
    ) -> None:
        manager.current_context().widget_data[self.widget_id] = page
        await self.on_page_changed.process_event(
            event,
            self.managed(manager),
            manager,
        )

    def managed(self, manager: DialogManager):
        return ManagedScrollingGroupAdapter(self, manager)


class ManagedScrollingGroupAdapter(ManagedWidget[ScrollingOrdersGroup]):
    def get_page(self) -> int:
        return self.widget.get_page(self.manager)

    async def set_page(self, page: int) -> None:
        return await self.widget.set_page(
            self.manager.event, page, self.manager,
        )
