from aiogram.fsm.state import StatesGroup, State

__all__ = ('PenaltyCreateStates',)


class PenaltyCreateStates(StatesGroup):
    staff = State()
    shift = State()
    reason = State()
    amount = State()
    photo = State()
    confirm = State()
