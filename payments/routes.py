from json.decoder import JSONDecodeError
from pydantic import ValidationError
from aiohttp import web
import utils

async def get_url(request: web.Request):
    try:
        data = await request.json()
        data = utils.Order(**data)
    except (JSONDecodeError, ValidationError):
        return web.Response(status=400)
    payment_url = await utils.get_url(data)
    return web.json_response({'payment_url': payment_url})
