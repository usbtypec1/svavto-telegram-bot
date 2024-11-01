from aiogram.fsm.state import StatesGroup, State

__all__ = ('ShiftFinishStates',)


class ShiftFinishStates(StatesGroup):
    statement_photo = State()
    service_app_photo = State()
    confirm = State()
