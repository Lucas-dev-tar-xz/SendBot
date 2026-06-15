from aiogram.fsm.state import State, StatesGroup


class AddAddress(StatesGroup):
    address = State()
    name = State()
