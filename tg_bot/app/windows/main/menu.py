from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import WebApp
from aiogram_dialog.widgets.text import Const

from tg_bot.states.states import MainSG

MainMenuWin = [
    Window(
        WebApp(url=Const('https://chatlabs.site/aokibot/frontend/'), text=Const('Магазин')),
        Const('Перейдите в магазин'),
        state=MainSG.main_menu,
    ),
]
