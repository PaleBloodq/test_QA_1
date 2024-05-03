import asyncio
import logging
import os
from typing import Union

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import ClientSession

rfn = {
    'category1': {
        'filters': [],
        'categoryies': {}
    }
}


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MyBot(metaclass=MetaSingleton):
    instance = None

    def getInstance(self):
        if self.instance is None:
            self.instance = Bot(token=os.environ.get('TELEGRAM_BOT_TOKEN'))
        return self.instance


class MyDispatcher(metaclass=MetaSingleton):
    instance = None

    def getInstance(self):
        if self.instance is None:
            self.instance = Dispatcher(storage=MemoryStorage())
        return self.instance


class ApiWrapper:
    session: ClientSession = None
    api_root_url: str = f"http://{os.environ.get('BACKEND_HOST','')}:{os.environ.get('BACKEND_PORT', '')}"
    timeout: int = 10

    @classmethod
    async def init_session(cls):
        if cls.session is None or cls.session.closed:
            cls.session = await aiohttp.ClientSession().__aenter__()

    @classmethod
    async def close_session(cls):
        if cls.session and not cls.session.closed:
            await cls.session.__aexit__(None, None, None)

    @classmethod
    async def _make_request(cls, method: str, url: str, data: dict = None, params: dict = None, expect_json = True) -> Union[bool, dict]:
        await cls.init_session()
        full_url = f"{cls.api_root_url}{url}"
        try:
            async with cls.session.request(method, full_url, json=data, params=params, timeout=cls.timeout) as response:
                if response.status == 200 and expect_json:
                    json_data = await response.json()
                    return json_data
                elif response.status == 200:
                    return True
                else:
                    return False
        except asyncio.TimeoutError:
            logging.warning('Request timed out')
            return False
        except aiohttp.ClientError as e:
            logging.warning(str(e))
            return False

    @classmethod
    async def get_token(cls, user_id: int) -> Union[bool, dict]:
        data = {'telegram_id': user_id}
        return await cls._make_request('POST', '/api/token/get/', data=data)

    @classmethod
    async def send_message(cls, order_id: str, text: str) -> Union[bool, dict]:
        data = {'order_id': order_id, 'text': text}
        return await cls._make_request('POST', '/api/order/chat/', data=data, expect_json=False)


def bootstrap():
    MyBot()
    MyDispatcher()
