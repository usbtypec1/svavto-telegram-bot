from mailbox import Message

from aiogram import Router, F
from aiogram.filters import StateFilter, invert_f
from aiogram.types import CallbackQuery

from callback_data import ShiftWorkTypeChoiceCallbackData
from enums import ShiftWorkType
from filters import admins_filter
from views.base import answer_view
from views.button_texts import ButtonText
from views.shifts import ShiftWorkTypeChoiceView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    ShiftWorkTypeChoiceCallbackData.filter(
        rule=F.work_type == ShiftWorkType.MOVE_TO_WASH,
    ),
    invert_f(admins_filter),
    StateFilter('*'),
)
async def on_move_to_wash_shift_work_type_choice(
        callback_query: CallbackQuery,
        callback_data: ShiftWorkTypeChoiceCallbackData,
) -> None:
    await callback_query.message.edit_text(
        'До 21:30 Вам придет уведомление в этот бот с запросом'
        ' <b>подтвердить или отклонить</b> выход на смену.'
        '\nПосле подтверждения, смена автоматически начнется.'
    )


@router.callback_query(
    ShiftWorkTypeChoiceCallbackData.filter(),
    invert_f(admins_filter),
    StateFilter('*'),
)
async def on_shift_work_type_choice(callback_query: CallbackQuery) -> None:
    await callback_query.answer('В разработке', show_alert=True)


@router.message(
    F.text == ButtonText.SHIFT_START,
    invert_f(admins_filter),
    StateFilter('*'),
)
async def on_show_shift_work_types_list(
        message: Message,
) -> None:
    await answer_view(message, ShiftWorkTypeChoiceView())
