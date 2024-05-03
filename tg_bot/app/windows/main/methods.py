from aiogram_dialog import DialogManager

import bootstrap


async def getter_token(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.middleware_data["event_from_user"].id
    response = await bootstrap.ApiWrapper.get_token(user_id=int(user_id))
    if response:
        return response
    await dialog_manager.reset_stack()