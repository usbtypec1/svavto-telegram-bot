from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from fast_depends import Depends, inject

from callback_data.prefixes import CallbackDataPrefix
from dependencies.repositories import get_staff_repository
from enums import StaffOrderBy
from filters import admins_filter
from repositories import StaffRepository
from views.base import answer_view, edit_message_by_view
from views.button_texts import ButtonText
from views.staff import StaffListView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.STAFF_LIST,
    admins_filter,
    StateFilter('*'),
)
@router.callback_query(
    F.data == CallbackDataPrefix.STAFF_LIST,
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_show_staff_list(
        message_or_callback_query: Message | CallbackQuery,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    staff_list = await staff_repository.get_all(
        order_by=StaffOrderBy.FULL_NAME_ASC,
    )
    view = StaffListView(staff_list)
    if isinstance(message_or_callback_query, Message):
        await answer_view(message_or_callback_query, view)
    else:
        await edit_message_by_view(message_or_callback_query.message, view)
