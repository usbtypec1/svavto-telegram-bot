from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from fast_depends import Depends, inject

from callback_data import StaffDetailCallbackData
from dependencies.repositories import get_staff_repository
from filters import admins_filter
from repositories import StaffRepository
from views.base import edit_message_by_view
from views.staff import StaffDetailView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    admins_filter,
    StaffDetailCallbackData.filter(),
    StateFilter('*'),
)
@inject
async def on_show_staff_detail(
        message: Message,
        callback_data: StaffDetailCallbackData,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    staff = await staff_repository.get_by_id(callback_data.telegram_id)
    view = StaffDetailView(staff)
    await edit_message_by_view(message, view)
