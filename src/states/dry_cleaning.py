from aiogram.fsm.state import State, StatesGroup


class DryCleaningRequestStates(StatesGroup):
    car_number = State()
    photos = State()
    services = State()
    confirm = State()
