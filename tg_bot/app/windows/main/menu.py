from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Url, Button
from aiogram_dialog.widgets.text import Const

from states.states import MainSG
from . import methods

MainMenuWin = [
    Window(
        Const("""
*Это не просто бот, а полноценный Playstation Store, но работающий в Telegram.*

Здесь есть:
• Кэшбэк система и оплата покупок баллами.
• Большой каталог игр, а так же различные скидки.
• Интересные подборки под разные интересы.
• Возможность оплачивать покупки со своей российской карты.

Теперь Вы можете покупать из России игры, подписки, донат и дополнения на свой турецкий аккаунт Playstation. 
А если у Вас его нет ещё нет - мы создадим его для Вас бесплатно!"""),
        # WebApp(url=Format(f'{os.environ.get("TELEGRAM_BOT_WEBAPP_URL")}?token={{token}}'), id='webapp', text=Const('Открыть магазин')),
        Button(Const("Ваши заказы📦"), id="test", on_click=methods.open_orders),
        Url(Const('Отзывы о нас'), url=Const('http://t.me/aoki_reviews'), id='rewiews'),
        Url(Const('Задать вопрос'), url=Const('http://t.me/aoki_psplus'), id='questions'),
        getter=methods.getter_token,
        parse_mode='markdown',
        state=MainSG.main_menu,
    ),
]
