from aiogram.fsm.state import StatesGroup, State

__all__ = ('CarWashCreateStates', 'CarWashRenameStates', 'CarWashDeleteStates')


class CarWashCreateStates(StatesGroup):
    name = State()
    confirm = State()


class CarWashRenameStates(StatesGroup):
    name = State()
    confirm = State()


class CarWashDeleteStates(StatesGroup):
    confirm = State()
