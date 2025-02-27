from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from fast_depends import inject

from callback_data import DeadSoulsMonthChooseCallbackData
from config import Config
from dependencies.repositories import (
    AvailableDateRepositoryDependency,
    ShiftRepositoryDependency,
)
from filters import admins_filter
from ui.views import answer_view, ButtonText, DeadSoulsMonthChooseView
from ui.views.supervision import DeadSoulsView

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
    view = DeadSoulsMonthChooseView(
        available_months=available_months,
        timezone=config.timezone,
    )
    await answer_view(message, view)


@router.callback_query(
    DeadSoulsMonthChooseCallbackData.filter(),
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_choose_month(
        callback_query: CallbackQuery,
        callback_data: DeadSoulsMonthChooseCallbackData,
        shift_repository: ShiftRepositoryDependency,
) -> None:
    dead_souls_for_month = await shift_repository.get_dead_souls(
        month=callback_data.month,
        year=callback_data.year,
    )
    view = DeadSoulsView(dead_souls_for_month)
    await answer_view(callback_query.message, view)
    await callback_query.answer()
