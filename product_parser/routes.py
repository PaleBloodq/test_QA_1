import asyncio
from json.decoder import JSONDecodeError
from pydantic import ValidationError
from aiohttp import web
import utils

async def parse(request: web.Request):
    try:
        data = await request.json()
        data = utils.Data(**data)
    except (JSONDecodeError, ValidationError):
        return web.Response(status=400)
    asyncio.create_task(utils.parse_product(data))
    return web.Response()
