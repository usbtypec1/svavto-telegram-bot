from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from filters import admins_filter
from views.base import answer_view
from views.button_texts import ButtonText
from views.mailing import MailingTypeChooseView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.MAILING,
    admins_filter,
    StateFilter('*'),
)
async def on_show_mailing_types(message: Message) -> None:
    view = MailingTypeChooseView()
    await answer_view(message, view)
