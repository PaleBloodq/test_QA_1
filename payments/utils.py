import os
import hashlib
import aiohttp
from pydantic import BaseModel, UUID4, NonNegativeFloat


TERMINAL_KEY = os.environ.get('TINKOFF_TERMINAL_KEY')
SECRET_KEY = os.environ.get('TINKOFF_SECRET_KEY')
if not (TERMINAL_KEY and SECRET_KEY):
    raise
API_URL = 'https://securepay.tinkoff.ru/v2/Init'


class Order(BaseModel):
    order_id: UUID4
    amount: NonNegativeFloat
    description: str
    customer_telegram_id: int


async def get_token(payment_data: dict):
    token_dict = {'Password': SECRET_KEY}
    for key in payment_data:
        if isinstance(payment_data[key], str):
            token_dict[key] = payment_data[key]
    token = ''.join(token_dict[key] for key in sorted(token_dict))
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


async def get_url(order: Order) -> str:
    payment_data = {
        'TerminalKey': TERMINAL_KEY,
        'OrderId': str(order.order_id),
        'Amount': str(int(order.amount * 100)),
        'Description': order.description,
        'Language': 'ru',
        'PayType': 'O',
        'Recurrent': 'N',
        'CustomerKey': str(order.customer_telegram_id),
    }
    payment_data['Token'] = await get_token(payment_data)
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=payment_data) as response:
            data = await response.json()
            return data.get('PaymentURL')
