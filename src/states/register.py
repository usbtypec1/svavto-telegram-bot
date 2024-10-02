from aiogram.fsm.state import StatesGroup, State

__all__ = ('PerformerRegisterStates',)


class PerformerRegisterStates(StatesGroup):
    full_name = State()
    car_sharing_phone_number = State()
    console_phone_number = State()
