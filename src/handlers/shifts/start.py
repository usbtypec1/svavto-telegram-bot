from mailbox import Message

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import ShiftWorkTypeChoiceCallbackData
from views.base import answer_view
from views.shifts import ShiftWorkTypeChoiceView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    ShiftWorkTypeChoiceCallbackData.filter(),
    StateFilter('*'),
)
async def on_shift_work_type_choice(
        callback_query: CallbackQuery,
        callback_data: ShiftWorkTypeChoiceCallbackData,
) -> None:
    await callback_query.message.answer(
        'До 21:30 Вам придет уведомление в этот бот с запросом подтвердить'
        ' или отклонить выход на смену.'
        '\nПосле подтверждения, смена автоматически начнется.'
    )


@router.message(
    F.text == 'Начать смену',
    StateFilter('*'),
)
async def on_show_shift_work_types_list(
        message: Message,
) -> None:
    await answer_view(message, ShiftWorkTypeChoiceView())
