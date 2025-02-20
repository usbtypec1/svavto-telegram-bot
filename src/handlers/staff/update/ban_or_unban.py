from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from fast_depends import Depends, inject

from callback_data import StaffUpdateCallbackData
from config import Config
from dependencies.repositories import get_staff_repository
from enums import StaffUpdateAction
from interactors import ChatUsernameReadInteractor
from repositories import StaffRepository
from ui.views import edit_message_by_view
from ui.views.staff import StaffDetailView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    StaffUpdateCallbackData.filter(
        rule=F.action.in_({StaffUpdateAction.BAN, StaffUpdateAction.UNBAN}),
    ),
    StateFilter('*'),
)
@inject
async def on_ban_or_unban_staff(
        callback_query: CallbackQuery,
        callback_data: StaffUpdateCallbackData,
        config: Config,
        bot: Bot,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    is_banned = callback_data.action == StaffUpdateAction.BAN
    await staff_repository.update_by_id(
        staff_id=callback_data.staff_id,
        is_banned=is_banned,
    )
    username = await ChatUsernameReadInteractor(
        bot=bot,
        chat_id=callback_data.staff_id,
    ).execute()
    staff = await staff_repository.get_by_id(callback_data.staff_id)
    view = StaffDetailView(
        staff=staff,
        web_app_base_url=config.web_app_base_url,
        include_banned=callback_data.include_banned,
        limit=callback_data.limit,
        offset=callback_data.offset,
        username=username,
    )
    await edit_message_by_view(callback_query.message, view)
