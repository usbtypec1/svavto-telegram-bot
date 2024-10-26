from aiogram.fsm.state import StatesGroup, State

__all__ = (
    'MailingToAllStates',
    'MailingToSpecificStaffStates',
    'MailingToLastActiveStaffStates',
)


class MailingToAllStates(StatesGroup):
    text = State()
    reply_markup = State()
    confirm = State()


class MailingToSpecificStaffStates(StatesGroup):
    text = State()
    reply_markup = State()
    chat_ids = State()


class MailingToLastActiveStaffStates(StatesGroup):
    text = State()
    reply_markup = State()
