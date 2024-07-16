from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    main_menu = State()


class OrderSG(StatesGroup):
    order_list = State()
    order = State()
    ps4 = State()
    ps5 = State()
    input_answer = State()
    no_options = State()


class TwoFaSG(StatesGroup):
    show = State()
