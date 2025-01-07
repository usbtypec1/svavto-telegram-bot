from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from filters import admins_filter
from models import SpecificShiftPickResult
from states import PenaltyCreateStates
from views.base import answer_text_view
from views.button_texts import ButtonText
from views.penalties import PenaltyCreateChooseReasonView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.web_app_data.button_text == ButtonText.SPECIFIC_SHIFT,
    admins_filter,
    StateFilter(PenaltyCreateStates.shift),
)
async def on_pick_specific_shift(
        message: Message,
        state: FSMContext,
) -> None:
    specific_shift_pick_result = SpecificShiftPickResult.model_validate_json(
        message.web_app_data.data,
    )
    await state.update_data(shift_id=specific_shift_pick_result.shift_id)
    await state.set_state(PenaltyCreateStates.reason)
    view = PenaltyCreateChooseReasonView()
    await message.answer(
        text='✅ Смена выбрана',
        reply_markup=ReplyKeyboardRemove(),
    )
    await answer_text_view(message, view)
