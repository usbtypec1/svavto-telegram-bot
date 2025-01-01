from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from fast_depends import Depends, inject

from callback_data import StaffDetailCallbackData
from config import Config
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
        callback_query: CallbackQuery,
        callback_data: StaffDetailCallbackData,
        config: Config,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    staff = await staff_repository.get_by_id(callback_data.staff_id)
    view = StaffDetailView(
        staff=staff,
        web_app_base_url=config.web_app_base_url,
        include_banned=callback_data.include_banned,
        limit=callback_data.limit,
        offset=callback_data.offset,
    )
    await edit_message_by_view(callback_query.message, view)
