from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    main_menu = State()


class OrderMessageSG(StatesGroup):
    message = State()
    input_answer = State()
