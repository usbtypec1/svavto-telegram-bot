from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from fast_depends import inject

from config import Config
from dependencies.repositories import ShiftRepositoryDependency
from filters import admins_filter
from interactors import ShiftsForSpecificDateReadInteractor
from services.shifts import get_current_shift_date
from ui.views import (
    answer_text_view, ButtonText,
    SupervisionShiftConfirmationsView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SUPERVISION_SHIFT_CONFIRMATIONS,
    admins_filter,
    StateFilter('*')
)
@inject
async def on_show_shift_confirmations(
        message: Message,
        config: Config,
        shift_repository: ShiftRepositoryDependency,
) -> None:
    shift_date = get_current_shift_date(config.timezone)

    shifts_for_today_read_interactor = ShiftsForSpecificDateReadInteractor(
        shift_repository=shift_repository,
        date=shift_date,
    )
    shifts = await shifts_for_today_read_interactor.execute()

    view = SupervisionShiftConfirmationsView(
        shift_date=shift_date,
        shifts=shifts,
    )
    await answer_text_view(message, view)
