from aiogram import Router

from aiogram.filters import StateFilter

from aiogram.types import CallbackQuery
from fast_depends import inject

from callback_data import ShiftConfirmCallbackData
from dependencies.repositories import ShiftRepositoryDependency
from ui.views import edit_as_confirmed


router = Router(name=__name__)


@router.callback_query(
    ShiftConfirmCallbackData.filter(),
    StateFilter('*'),
)
@inject
async def on_confirm_shift(
        callback_query: CallbackQuery,
        callback_data: ShiftConfirmCallbackData,
        shift_repository: ShiftRepositoryDependency,
) -> None:
    await shift_repository.confirm(shift_id=callback_data.shift_id)
    await callback_query.answer(
        '✅ Вы подтвердили выход на смену',
        show_alert=True,
    )
    await edit_as_confirmed(callback_query.message)
