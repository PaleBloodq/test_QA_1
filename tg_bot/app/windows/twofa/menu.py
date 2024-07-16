from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Button, Back
from aiogram_dialog.widgets.text import Const

from app.windows.order.handlers import process_yes
from app.windows.twofa.handlers import process_no_ps4, process_no_ps5
from states.states import TwoFaSG
from texts import TWOFA_TEXT, TWOFA_START, TWOFA_PS4, TWOFA_PS5

TwoFaWin = [
    Window(
        Const(TWOFA_START),
        Button(Const('ps 4'), id='ps4', on_click=process_no_ps4),
        Button(Const('ps 5'), id='ps5', on_click=process_no_ps5),
        Cancel(Const('Выход'), id='back'),
        state=TwoFaSG.wtf_2fa,
    ),
    Window(
        Const(TWOFA_PS4),
        Button(Const('Сорян, у меня ps 5'), id='ps5', on_click=process_no_ps5),
        Cancel(Const('Выход'), id='back'),
        state=TwoFaSG.ps4,
    ),
    Window(
        Const(TWOFA_PS5),
        Button(Const('ФАААААААААК, у меня ps 4'), id='ps4', on_click=process_no_ps4),
        Cancel(Const('Выход'), id='back'),
        state=TwoFaSG.ps5,
    )
]
