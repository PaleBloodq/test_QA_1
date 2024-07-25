from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Button, Back, SwitchTo, Row
from aiogram_dialog.widgets.text import Const

from . import methods
from states.states import TwoFaSG
import texts

TwoFaWin = [
    Window(
        Const(texts.TWOFA_START_TEXT),
        Row(SwitchTo(Const('Да'), id='send_code', state=TwoFaSG.send_code),
        SwitchTo(Const('Нет'), id='tutorial', state=TwoFaSG.tutorial)),
        Cancel(Const('Назад'), id='back'),
        state=TwoFaSG.show,
    ),
    Window(
        Const(texts.TWOFA_SEND_CODE_TEXT),
        MessageInput(func=methods.send_code, content_types=['text']),
        SwitchTo(Const('Назад'), id='back', state=TwoFaSG.show),
        state=TwoFaSG.send_code,
    ),
    Window(
        Const(texts.TWOFA_TUTORIAL_TEXT),
        Row(SwitchTo(Const('Включил'), id='send_code', state=TwoFaSG.send_code),
        Button(Const('Не получается'), id='get_help', on_click=methods.get_help)),
        SwitchTo(Const('Назад'), id='back', state=TwoFaSG.show),
        state=TwoFaSG.tutorial,
    )
]