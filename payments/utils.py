import os
import logging
import hashlib
import aiohttp
from pydantic import BaseModel, UUID4, NonNegativeFloat, Field


TERMINAL_KEY = os.environ.get('TINKOFF_TERMINAL_KEY')
SECRET_KEY = os.environ.get('TINKOFF_SECRET_KEY')
if not (TERMINAL_KEY and SECRET_KEY):
    raise

API_URL = 'https://securepay.tinkoff.ru/v2/'

PAYMENT_WEBHOOK_URL = os.environ.get("PAYMENT_WEBHOOK_URL")


class OrderItem(BaseModel):
    name: str
    price: NonNegativeFloat
    quantity: int
    amount: NonNegativeFloat


class Order(BaseModel):
    order_id: UUID4
    amount: NonNegativeFloat
    description: str
    customer_telegram_id: int
    bill_email: str
    items: list[OrderItem]


class Payment(BaseModel):
    payment_id: str = Field(alias='PaymentId')
    payment_url: str = Field(alias='PaymentURL')


async def get_token(payment_data: dict):
    token_dict = {'Password': SECRET_KEY}
    for key in payment_data:
        if isinstance(payment_data[key], str):
            token_dict[key] = payment_data[key]
        elif isinstance(payment_data[key], bool):
            token_dict[key] = 'true' if payment_data[key] else 'false'
        elif isinstance(payment_data[key], int):
            token_dict[key] = str(payment_data[key])
    token = ''.join(token_dict[key] for key in sorted(token_dict))
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


async def create_payment(order: Order) -> Payment | None:
    payment_data = {
        'TerminalKey': TERMINAL_KEY,
        'OrderId': str(order.order_id),
        'Amount': str(int(order.amount * 100)),
        'Description': order.description,
        'Language': 'ru',
        'PayType': 'O',
        'Recurrent': 'N',
        'CustomerKey': str(order.customer_telegram_id),
        'NotificationURL': PAYMENT_WEBHOOK_URL,
    }
    payment_data['Token'] = await get_token(payment_data)
    payment_data['Receipt'] = {
        'FfdVersion': '1.2',
        'Taxation': 'usn_income',
        'Email': order.bill_email,
        'Items': [
            {
                'Name': item.name,
                'Price': int(item.price * 100),
                'Quantity': 1,
                'Amount': int(item.amount * 100),
                'Tax': 'none',
                'PaymentMethod': 'partial_payment',
                'PaymentObject': 'commodity',
                'MeasurementUnit': 'шт.',
            } for item in order.items
        ],
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(API_URL+'Init', json=payment_data) as response:
                payment = await response.json()
            payment_id = payment.get('PaymentId')
            get_qr_data = {
                'TerminalKey': TERMINAL_KEY,
                'PaymentId': payment_id,
                'DataType': 'PAYLOAD',
            }
            get_qr_data['Token'] = await get_token(get_qr_data)
            async with session.post(API_URL+'GetQr', json=get_qr_data) as response:
                qr = await response.json()
            payment_url = qr.get('Data')
            return Payment(PaymentId=payment_id, PaymentURL=payment_url)
        except Exception as exc:
            logging.exception(exc)


async def get_payment(payment_id: str) -> dict:
    payment_data = {
        'TerminalKey': TERMINAL_KEY,
        'PaymentId': payment_id,
    }
    payment_data['Token'] = await get_token(payment_data)
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL+'GetState', json=payment_data) as response:
            return await response.json()


async def check_token(data: dict) -> bool:
    token = data.pop('Token', None)
    if token:
        expected_token = await get_token(data)
        return expected_token == token
    return False
