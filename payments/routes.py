from json.decoder import JSONDecodeError
from pydantic import ValidationError
from aiohttp import web
import utils


async def create_payment(request: web.Request):
    try:
        data = await request.json()
        data = utils.Order(**data)
    except (JSONDecodeError, ValidationError):
        return web.Response(status=400)
    payment = await utils.create_payment(data)
    if payment:
        return web.json_response(payment.model_dump(mode='json'))


async def get_payment(request: web.Request):
    try:
        data = await request.json()
        payment_id = data.get('PaymentId')
    except (JSONDecodeError, ValidationError):
        return web.Response(status=400)
    status = await utils.get_payment(payment_id)
    if status:
        return web.json_response(status)

async def check_token(request: web.Request):
    try:
        data = await request.json()
    except JSONDecodeError:
        return web.Response(status=400)
    token_correct = await utils.check_token(data)
    return web.json_response({'TokenCorrect': token_correct})
