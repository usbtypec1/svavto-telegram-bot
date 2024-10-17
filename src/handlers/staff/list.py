from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from fast_depends import Depends, inject

from dependencies.repositories import get_staff_repository
from filters import admins_filter
from repositories import StaffRepository
from views.base import answer_view
from views.button_texts import ButtonText
from views.staff import StaffListView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.STAFF_LIST,
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_show_staff_list(
        message: Message,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    staff_list = await staff_repository.get_all()
    view = StaffListView(staff_list)
    await answer_view(message, view)
