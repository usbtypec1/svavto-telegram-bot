from aiogram.fsm.state import StatesGroup, State

__all__ = (
    'ShiftFinishStates',
    'ShiftTestStartStates',
    'ShiftTodayStartStates',
    'ShiftExtraStartStates',
    'ShiftRegularStartStates',
)


class ShiftFinishStates(StatesGroup):
    statement_photo = State()
    service_app_photo = State()
    confirm = State()


class ShiftTestStartStates(StatesGroup):
    car_wash = State()


class ShiftExtraStartStates(StatesGroup):
    car_wash = State()


class ShiftTodayStartStates(StatesGroup):
    car_wash = State()


class ShiftRegularStartStates(StatesGroup):
    car_wash = State()
