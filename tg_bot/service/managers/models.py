from typing import Optional

from aiogram.types import CallbackQuery
from pydantic import BaseModel

from web.api.models import Order


class UserModel(BaseModel):
    token: Optional[str] = None
    selected_order: Optional[Order] = None
