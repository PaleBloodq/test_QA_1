from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp.abc import Request
from aiohttp.web_response import Response

from tg_bot import bootstrap
from tg_bot.web.api.models import NewMessage, NewPayment

bot = bootstrap.MyBot().getInstance()


async def send_message_manager(request: Request) -> Response:
    data = await request.json()
    try:
        data = NewMessage(**data)
        text = f"Сообщение от менеджера по заказу №{data.order_id}\n" + data.text
        await bot.send_message(data.user_id, text=text)
    except Exception as e:
        print(e)
        return Response(status=400)
    return Response()


async def send_message_payment(request: Request) -> Response:
    data = await request.json()
    try:
        data = NewPayment(**data)
        text = f"Отлично! по заказу №{data.order_id} прошла оплата.\n\n"
        text += "Чтобы успешно войти в ваш аккаунт на нём должна быть включена двухфакторная аутентификация (но мы зовём её просто духфакторкой). Без неё сайт PlayStation будет чаще сбоить.\n\n"
        text += "Если у вас она есть, то отправьте резервные коды ответом на это сообщение, мы все сделаем.\n" \
                "Если нет то обратитесь к соответсвующему пункту меню и возвращайтесь к этому сообщению)\n" \
                "Если совсем не можете разобраться, напишите свои вопросы ответом на это сообщение, и совсем скоро мы вам ответим!"
        await bot.send_message(data.user_id, text=text)
    except Exception as e:
        print(e)
        return Response(status=400)
    return Response()
