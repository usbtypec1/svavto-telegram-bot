from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from fast_depends import Depends, inject

from callback_data import StaffUpdateCallbackData
from config import Config
from dependencies.repositories import get_staff_repository
from enums import StaffType, StaffUpdateAction
from interactors import ChatUsernameReadInteractor
from repositories import StaffRepository
from ui.views import edit_message_by_view
from ui.views.staff import StaffDetailView


__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    StaffUpdateCallbackData.filter(
        rule=F.action.in_(
            {
                StaffUpdateAction.TO_CAR_TRANSPORTER_AND_WASHER,
                StaffUpdateAction.TO_CAR_TRANSPORTER,
            },
        ),
    ),
    StateFilter('*'),
)
@inject
async def on_staff_type_change(
        callback_query: CallbackQuery,
        callback_data: StaffUpdateCallbackData,
        config: Config,
        bot: Bot,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    if callback_data.action == StaffUpdateAction.TO_CAR_TRANSPORTER:
        staff_type = StaffType.CAR_TRANSPORTER
    else:
        staff_type = StaffType.CAR_TRANSPORTER_AND_WASHER

    staff = await staff_repository.get_by_id(callback_data.staff_id)
    await staff_repository.update_by_id(
        staff_id=callback_data.staff_id,
        is_banned=staff.is_banned,
        staff_type=staff_type,
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
