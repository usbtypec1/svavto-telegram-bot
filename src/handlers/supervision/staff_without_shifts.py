from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from fast_depends import inject

from callback_data import StaffWithoutShiftsMonthChooseCallbackData
from config import Config
from dependencies.repositories import (
    AvailableDateRepositoryDependency,
    ShiftRepositoryDependency,
)
from filters import admins_filter
from ui.views import answer_view, ButtonText, StaffWithoutShiftsMonthChooseView
from ui.views.supervision.staff_without_shifts import StaffWithoutShiftsView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SUPERVISION_STAFF_WITHOUT_SHIFTS,
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_show_available_months(
        message: Message,
        config: Config,
        available_date_repository: AvailableDateRepositoryDependency,
) -> None:
    available_months = await available_date_repository.get_all()
    view = StaffWithoutShiftsMonthChooseView(
        available_months=available_months,
        timezone=config.timezone,
    )
    await answer_view(message, view)


@router.callback_query(
    StaffWithoutShiftsMonthChooseCallbackData.filter(),
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_choose_month(
        callback_query: CallbackQuery,
        callback_data: StaffWithoutShiftsMonthChooseCallbackData,
        shift_repository: ShiftRepositoryDependency,
) -> None:
    staff_without_shifts = await shift_repository.get_staff_without_shifts(
        month=callback_data.month,
        year=callback_data.year,
    )
    view = StaffWithoutShiftsView(staff_without_shifts)
    await answer_view(callback_query.message, view)
    await callback_query.answer()
