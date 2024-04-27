import os
import hashlib
import asyncio
import aiohttp

class Payments:
    def __init__(self) -> None:
        self.terminal_key = os.environ.get('TINKOFF_TERMINAL_KEY', '1714050593375DEMO')
        self.secret_key = os.environ.get('TINKOFF_SECRET_KEY', 'bzva656tfmvzxxfz')
        if not (self.terminal_key or self.secret_key):
            raise
        self.api_url = "https://securepay.tinkoff.ru/v2/Init"
    
    async def get_token(self, payment_data: dict):
        token_dict = {'Password': self.secret_key}
        for key in payment_data:
            if isinstance(payment_data[key], str):
                token_dict[key] = payment_data[key]
        token = ''
        for key in sorted(token_dict):
            token += str(token_dict[key])
        return hashlib.sha256(token.encode('utf-8')).hexdigest()
    
    async def get_url(self, order_id: str, amount: float, description: str, customer_telegram_id: int) -> str:
        amount = str(int(amount * 100))
        customer_key = str(customer_telegram_id)
        payment_data = {
            'TerminalKey': self.terminal_key,
            'OrderId': order_id,
            'Amount': amount,
            'Description': description,
            'Language': 'ru',
            'PayType': 'O',
            'Recurrent': 'N',
            'CustomerKey': customer_key,
        }
        payment_data['Token'] = await self.get_token(payment_data)
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=payment_data) as response:
                data = await response.json()
                return data.get('PaymentURL')

async def main():
    payments = Payments()
    paymnet_data = await payments.get_payment_data(
        'f59a6f47-e11d-4a72-94db-059eae8a0a90',
        10.3,
        'Тестовая покупка',
        518485500,
    )
    return await payments.get_url(paymnet_data)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
