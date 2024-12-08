from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class UsernameInputState(StatesGroup):
    entering_username = State()
