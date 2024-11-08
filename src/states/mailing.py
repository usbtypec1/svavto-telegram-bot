from aiogram.fsm.state import StatesGroup, State

__all__ = (
    'MailingToAllStates',
    'MailingToSpecificStaffStates',
    'MailingToLastActiveStaffStates',
    'MailingStates',
)


class MailingStates(StatesGroup):
    type = State()
    text = State()
    reply_markup = State()
    photos = State()
    chat_ids = State()
    confirm = State()


class MailingToAllStates(MailingStates):
    pass


class MailingToSpecificStaffStates(MailingStates):
    chat_ids = State()


class MailingToLastActiveStaffStates(MailingStates):
    pass
