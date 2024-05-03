import asyncio
import os

from aiogram.types import BotCommandScopeDefault, BotCommand
from aiogram_dialog import setup_dialogs
from aiohttp import web

import bootstrap
from .app import register_dialogs
from .app.dialogs import error_handler
from .app.routes import register_routes

from .web.api.routes import send_message_manager, send_message_payment

app = web.Application()
app.add_routes([web.post('/api/order/message/send/', send_message_manager),
                web.post('/api/order/payment/access/', send_message_payment),])


async def main():
    bootstrap.bootstrap()
    bot = bootstrap.MyBot().getInstance()
    dp = bootstrap.MyDispatcher().getInstance()
    dp.errors.register(error_handler)
    register_routes(dp)
    register_dialogs(dp)
    setup_dialogs(dp)
    print(dp.sub_routers)
    await bot.set_my_commands([BotCommand(command="start", description="Запустить бота")],
                              scope=BotCommandScopeDefault())
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get('TELEGRAM_BOT_PORT')))
    print(site.name)
    await site.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
