from aiogram.fsm.state import StatesGroup, State

__all__ = ('ShiftFinishStates', 'ShiftStartStates')


class ShiftFinishStates(StatesGroup):
    statement_photo = State()
    service_app_photo = State()
    confirm = State()


class ShiftStartStates(StatesGroup):
    car_wash = State()
