import asyncio
import os

from aiogram.types import BotCommandScopeDefault, BotCommand
from aiogram_dialog import setup_dialogs
from aiohttp import web

import bootstrap
from app import register_dialogs
from app.dialogs import error_handler
from app.routes import register_routes

from web.api.routes import send_message_manager, change_order, mailing

app = web.Application()
app.add_routes([
    web.post('/api/order/message/send/', send_message_manager),
    web.post('/api/order/change/', change_order),
    web.post('/api/mailing/', mailing),
])


async def main():
    bootstrap.bootstrap()
    bot = bootstrap.MyBot().getInstance()
    dp = bootstrap.MyDispatcher().getInstance()
    dp.errors.register(error_handler)
    register_routes(dp)
    register_dialogs(dp)
    setup_dialogs(dp)
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
