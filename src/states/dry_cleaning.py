from aiogram.fsm.state import State, StatesGroup


class DryCleaningRequestStates(StatesGroup):
    car = State()
