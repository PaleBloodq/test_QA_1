from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from states.states import TwoFaSG


async def process_no(c: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await c.answer("Вы нажали Нет")
    await dialog_manager.switch_to(TwoFaSG.wtf_2fa)


async def process_no_ps4(c: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await c.answer("Вы выбрали ps 4")
    await dialog_manager.switch_to(TwoFaSG.ps4)


async def process_no_ps5(c: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await c.answer("Вы выбрали ps 5")
    await dialog_manager.switch_to(TwoFaSG.ps5)