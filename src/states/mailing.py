from aiogram.fsm.state import StatesGroup, State

__all__ = ('MailingStates',)


class MailingStates(StatesGroup):
    type = State()
    text = State()
    reply_markup = State()
    photos = State()
    chat_ids = State()
    confirm = State()
