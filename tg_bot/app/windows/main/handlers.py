import logging

from aiogram import types
from aiogram_dialog import DialogManager

import bootstrap
from service.managers.user_data_manager import UserData
from states.states import MainSG


async def start(message: types.Message, dialog_manager: DialogManager | None = None):
    user_id = message.chat.id
    response = await bootstrap.ApiWrapper.get_token(user_id=int(user_id))
    logging.warning(response)
    if response:
        UserData.get_data(user_id).token = response.get('token')
        await dialog_manager.start(state=MainSG.main_menu)
    else:
        await dialog_manager.reset_stack()


