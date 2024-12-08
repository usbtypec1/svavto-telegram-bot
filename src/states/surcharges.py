from aiogram.fsm.state import StatesGroup, State

__all__ = ('SurchargeCreateStates',)


class SurchargeCreateStates(StatesGroup):
    staff = State()
    shift = State()
    reason = State()
    amount = State()
    confirm = State()
