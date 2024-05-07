from dataclasses import dataclass
from typing import Literal, List, Optional

from pydantic import BaseModel

import texts


@dataclass
class OrderExtra:
    status_text: str
    emoji: str
    text: str


class NewMessage(BaseModel):
    order_id: str
    text: str
    user_id: int


class OrderProduct(BaseModel):
    item: str
    description: str
    final_price: int


class Order(BaseModel):
    user_id: int
    order_id: str
    date: str
    amount: int
    order_products: Optional[List[OrderProduct]]
    payment_url: Optional[str]
    need_account: bool
    status: Literal['IN_PROGRESS', 'COMPLETED', 'ERROR', 'PAID', 'PAYMENT']

    def get_order_extra(self) -> Optional[OrderExtra]:
        match self.status:
            case 'IN_PROGRESS':
                return OrderExtra(status_text='В обработке', emoji='⏳', text=texts.IN_PROGRESS_TEXT)
            case 'COMPLETED':
                return OrderExtra(status_text='Завершен', emoji='✅', text=texts.COMPLETED_TEXT)
            case 'ERROR':
                return OrderExtra(status_text='Ошибка', emoji='❌', text=texts.ERROR_TEXT)
            case 'PAID':
                if self.need_account:
                    text = texts.PAID_NEED_ACCOUNT_TEXT
                else:
                    text = texts.PAID_TEXT
                return OrderExtra(status_text='Оплачен', emoji='💰', text=text)
            case 'PAYMENT':
                return OrderExtra(status_text='Ожидает оплаты', emoji='💳', text=texts.PAYMENT_TEXT)

    def get_normalized_products(self):
        if self.order_products:
            texts = [f'•{product.item} — {product.final_price}\n' for product in self.order_products]
            return ''.join(texts)
        return ''


class OrderList(BaseModel):
    orders: List[Order]
