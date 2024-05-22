from aiogram.types import User, Chat
from aiogram_dialog.manager.bg_manager import BgManager
import re

import bootstrap

bot = bootstrap.MyBot().getInstance()
dp = bootstrap.MyDispatcher().getInstance()


async def create_bg_manager(user_id: int) -> BgManager:
    user = User(id=user_id, is_bot=False, first_name="First name")
    chat = Chat(id=user_id, type="private")
    return BgManager(user=user, chat=chat, bot=bot, router=dp.sub_routers[0], intent_id=None, stack_id="",
                     load=True)



def escape_markdown(text):
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)