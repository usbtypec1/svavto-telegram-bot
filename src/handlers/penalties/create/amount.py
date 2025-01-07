from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import admins_filter
from services.validators import parse_integer_number
from states import PenaltyCreateStates
from views.base import answer_text_view
from views.penalties import PenaltyPhotoInputView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text,
    admins_filter,
    StateFilter(PenaltyCreateStates.amount),
)
async def on_input_amount_for_penalty(
        message: Message,
        state: FSMContext,
) -> None:
    amount = parse_integer_number(message.text)
    await state.update_data(amount=amount)
    await state.set_state(PenaltyCreateStates.photo)
    view = PenaltyPhotoInputView()
    await answer_text_view(message, view)
