from aiogram.fsm.state import StatesGroup, State

__all__ = ('PenaltyCreateStates',)


class PenaltyCreateStates(StatesGroup):
    staff = State()
    reason = State()
    confirm = State()
