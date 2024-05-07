from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from states.states import TwoFaSG
from texts import TWOFA_TEXT

TwoFaWin = [
    Window(
        Const(TWOFA_TEXT),
        Cancel(Const('Назад'), id='back'),
        state=TwoFaSG.show,
    ),
]
