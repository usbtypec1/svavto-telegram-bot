from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from fast_depends import Depends, inject

from callback_data import StaffListCallbackData
from callback_data.prefixes import CallbackDataPrefix
from dependencies.repositories import get_staff_repository
from enums import StaffOrderBy
from filters import admins_filter
from repositories import StaffRepository
from ui.views import answer_text_view, edit_message_by_view
from ui.views import ButtonText
from ui.views.staff import StaffListView, StaffMenuView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    StaffListCallbackData.filter(),
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_show_staff_list_all(
        callback_query: CallbackQuery,
        callback_data: StaffListCallbackData,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    staff_list_page = await staff_repository.get_all(
        order_by=StaffOrderBy.FULL_NAME_ASC,
        include_banned=callback_data.include_banned,
        limit=callback_data.limit,
        offset=callback_data.offset,
    )
    view = StaffListView(
        staff_list_page=staff_list_page,
        include_banned=callback_data.include_banned
    )
    await edit_message_by_view(callback_query.message, view)
    await callback_query.answer()


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
) -> None:
    view = StaffMenuView()
    if isinstance(message_or_callback_query, Message):
        await answer_text_view(message_or_callback_query, view)
    else:
        await edit_message_by_view(message_or_callback_query.message, view)
