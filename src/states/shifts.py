from aiogram.fsm.state import StatesGroup, State

__all__ = ('ShiftAddCarStates',)


class ShiftAddCarStates(StatesGroup):
    car_number = State()
    car_class = State()
    wash_type = State()
    is_windshield_washer_refilled = State()
    windshield_washer_refilled_value = State()
    has_additional_services = State()
    additional_services = State()
    confirm = State()
