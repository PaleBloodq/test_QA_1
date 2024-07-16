from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    main_menu = State()


class OrderSG(StatesGroup):
    order_list = State()
    order = State()
    input_answer = State()


class TwoFaSG(StatesGroup):
    show = State()
    wtf_2fa = State()
    ps4 = State()
    ps5 = State()
