from dataclasses import dataclass
from typing import Literal, List, Optional

from pydantic import BaseModel, field_validator

import texts
import utils


@dataclass
class OrderExtra:
    status_text: str
    emoji: str
    text: str

    def __post_init__(self):
        self.text = utils.escape_markdown(self.text)


class NewMessage(BaseModel):
    order_id: str
    text: str
    user_id: int
    images: Optional[List[str]] = None


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

    @field_validator('order_id', 'date')
    def process_text_fields(cls, value):
        if isinstance(value, str):
            return utils.escape_markdown(value)
        return value

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


class MailingButton(BaseModel):
    url: str
    text: str


class Mailing(BaseModel):
    id: str
    text: str
    telegram_ids: list[int]
    media: list[str]
    buttons: list[MailingButton]
