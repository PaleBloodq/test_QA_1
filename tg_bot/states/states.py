from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    main_menu = State()


class OrderSG(StatesGroup):
    order_list = State()
    order = State()
    input_answer = State()

class TwoFaSG(StatesGroup):
    show = State()
