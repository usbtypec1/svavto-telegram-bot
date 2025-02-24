from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from fast_depends import inject

from callback_data import ShiftRejectCallbackData
from dependencies.repositories import ShiftRepositoryDependency
from ui.views import edit_as_rejected


router = Router(name=__name__)


@router.callback_query(
    ShiftRejectCallbackData.filter(),
    StateFilter('*'),
)
@inject
async def on_reject_shift(
        callback_query: CallbackQuery,
        callback_data: ShiftRejectCallbackData,
        shift_repository: ShiftRepositoryDependency,
) -> None:
    await shift_repository.reject(shift_id=callback_data.shift_id)
    await callback_query.answer(
        '❗️ Вы отклонили выход на смену',
        show_alert=True,
    )
    await edit_as_rejected(callback_query.message)
