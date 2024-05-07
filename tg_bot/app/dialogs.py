import logging

from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram_dialog import Dialog, LaunchMode
from aiogram_dialog.api.exceptions import UnknownIntent

import bootstrap
from .windows.main.menu import MainMenuWin
from .windows.order.menu import OrderWin
from .windows.twofa.menu import TwoFaWin

bot = bootstrap.MyBot().getInstance()


async def error_handler(event):
    logging.error(str(event.exception))
    if isinstance(event.exception, UnknownIntent):
        if event.update.callback_query:
            try:
                await event.update.callback_query.message.delete()
            except:
                await event.update.callback_query.answer()
        elif event.update.message:
            try:
                await event.update.callback_query.message.delete()
            except:
                await bot.send_message(event.update.message.chat.id, "/start")
    else:
        return UNHANDLED


DLGS = (Dialog(*MainMenuWin, launch_mode=LaunchMode.ROOT),
        Dialog(*OrderWin, launch_mode=LaunchMode.ROOT),
        Dialog(*TwoFaWin, launch_mode=LaunchMode.SINGLE_TOP),)
