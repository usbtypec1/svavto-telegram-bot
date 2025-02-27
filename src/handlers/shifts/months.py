from aiogram import F, Router
from aiogram.filters import invert_f, StateFilter
from aiogram.types import CallbackQuery, Message
from fast_depends import inject

from callback_data import ShiftMonthChoiceCallbackData
from config import Config
from dependencies.repositories import ShiftRepositoryDependency
from filters import admins_filter
from interactors import ShiftsOfMonthReadInteractor
from ui.views import (
    answer_view, AvailableMonthsListView, ButtonText,
    ShiftsForMonthListView,
)


__all__ = ('router',)

router = Router(name=__name__)

@router.callback_query(ShiftMonthChoiceCallbackData.filter(), StateFilter('*'))
@inject
async def on_choose_shift_month(
        callback_query: CallbackQuery,
        callback_data: ShiftMonthChoiceCallbackData,
        shift_repository: ShiftRepositoryDependency,
) -> None:
    shifts = await ShiftsOfMonthReadInteractor(
        shift_repository=shift_repository,
        month=callback_data.month,
        year=callback_data.year,
        staff_id=callback_query.from_user.id
    ).execute()
    view = ShiftsForMonthListView(
        month=callback_data.month,
        year=callback_data.year,
        shifts=shifts,
    )
    await answer_view(callback_query.message, view)


@router.message(
    F.text == ButtonText.SHIFT_MONTH_LIST,
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_show_staff_shift_month_list(
        message: Message,
        config: Config,
        shift_repository: ShiftRepositoryDependency,
) -> None:
    staff_shift_months = await shift_repository.get_months(
        staff_id=message.from_user.id,
    )
    view = AvailableMonthsListView(
        available_months=staff_shift_months.months,
        timezone=config.timezone,
        callback_data_factory=ShiftMonthChoiceCallbackData,
    )
    await answer_view(message, view)
