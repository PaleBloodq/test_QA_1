from typing import Optional

from aiogram_dialog import DialogManager

import bootstrap
from .models import UserModel

class UserData:
    users_data = {}

    def __init__(self, dialog_manager: DialogManager):
        self.dialog_manager = dialog_manager
        self.user_id = self.get_user_id(dialog_manager)
        self.data: Optional[UserModel] = self._get_data(self.user_id)
    @staticmethod
    def _get_data(user_id) -> UserModel:
        if user_id in UserData.users_data:
            data = UserData.users_data[user_id]
        else:
            data = UserModel()
            UserData.users_data[user_id] = data
        return data

    @classmethod
    def get_data(cls, user_id: int) -> UserModel:
        return cls._get_data(user_id)

    @classmethod
    def get_data_by_id(cls, user_id: str):
        return cls.get_data(user_id)
    @classmethod
    def get_user_id(cls, dialog_manager: DialogManager):
        return dialog_manager.middleware_data["event_from_user"].id
