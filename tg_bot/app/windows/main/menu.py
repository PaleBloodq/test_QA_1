from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import WebApp, Button, Start
from aiogram_dialog.widgets.text import Const, Format

from .methods import getter_token, open_orders
from states.states import MainSG, TwoFaSG

MainMenuWin = [
    Window(
        Const('Перейдите в магазин'),
        WebApp(url=Format('https://chatlabs.site/aokibot/frontend/?token={token}'), id='webapp', text=Const('Магазин')),
        Button(Const("Ваши заказы📦"), id="test", on_click=open_orders),
        Start(Const('Как включить 2FA?'), state=TwoFaSG.show, id='2FA'),
        getter=getter_token,
        state=MainSG.main_menu,
    ),
]
