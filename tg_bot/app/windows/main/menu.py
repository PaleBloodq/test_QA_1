from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import WebApp
from aiogram_dialog.widgets.text import Const, Format

from .methods import getter_token
from states.states import MainSG

MainMenuWin = [
    Window(
        WebApp(url=Format('https://chatlabs.site/aokibot/frontend?token={token}'), text=Const('Магазин')),
        Const('Перейдите в магазин'),
        getter=getter_token,
        state=MainSG.main_menu,
    ),
]
