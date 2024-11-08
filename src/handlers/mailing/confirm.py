from collections.abc import Iterable
from datetime import UTC, datetime

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from fast_depends import Depends, inject

from callback_data.prefixes import CallbackDataPrefix
from config import Config
from dependencies.repositories import get_staff_repository
from enums import MailingType, StaffOrderBy
from filters import admins_filter
from models import Staff
from repositories import StaffRepository
from services.notifications import MailingService
from states import MailingStates
from aiogram import Router
from dependencies.services import get_maling_service

__all__ = ('router',)

from views.admins import AdminMenuView
from views.base import answer_view

router = Router(name=__name__)


@router.callback_query(
    F.data == CallbackDataPrefix.MAILING_CREATE_ACCEPT,
    admins_filter,
    StateFilter(MailingStates.confirm)
)
@inject
async def on_confirm_mailing(
        callback_query: CallbackQuery,
        state: FSMContext,
        config: Config,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
        mailing_service: MailingService = Depends(
            dependency=get_maling_service,
            use_cache=False,
        ),
) -> None:
    state_data: dict = await state.get_data()
    await state.clear()

    mailing_type: MailingType = state_data['type']
    text: str = state_data['text']
    photo_file_ids: list[str] = state_data.get('photo_file_ids', [])
    chat_ids: list[int] = state_data.get('chat_ids', [])
    reply_markup_json: str | None = state_data.get('reply_markup')

    reply_markup = (
        None if reply_markup_json is None
        else InlineKeyboardMarkup.model_validate_json(reply_markup_json)
    )

    def filter_staff_by_chat_ids(
            *,
            staff_list: Iterable[Staff],
            chat_ids: Iterable[int],
    ) -> list[Staff]:
        chat_ids = set(chat_ids)
        return [staff for staff in staff_list if staff.id in chat_ids]

    def filter_banned_staff(
            staff_list: Iterable[Staff],
    ) -> list[Staff]:
        return [staff for staff in staff_list if not staff.is_banned]

    def filter_last_active_staff(
            staff_list: Iterable[Staff],
            last_activity_days: int,
    ) -> list[Staff]:
        result: list[Staff] = []
        now = datetime.now(UTC)
        for staff in staff_list:
            time_since_last_activity = now - staff.last_activity_at
            if time_since_last_activity.days < last_activity_days:
                result.append(staff)
        return result

    staff_list = await staff_repository.get_all(
        order_by=StaffOrderBy.LAST_ACTIVITY_AT_DESC
    )
    staff_list = filter_banned_staff(staff_list)

    if mailing_type.SPECIFIC_STAFF:
        staff_list = filter_staff_by_chat_ids(
            staff_list=staff_list,
            chat_ids=chat_ids,
        )
    elif mailing_type.LAST_ACTIVE:
        staff_list = filter_last_active_staff(
            staff_list=staff_list,
            last_activity_days=30,
        )

    chat_ids = [staff.id for staff in staff_list]

    if len(photo_file_ids) == 0:
        await mailing_service.send_text(
            chat_ids=chat_ids,
            text=text,
            reply_markup=reply_markup,
        )
    elif len(photo_file_ids) == 1:
        await mailing_service.send_single_photo(
            chat_ids=chat_ids,
            text=text,
            photo_file_id=photo_file_ids[0],
            reply_markup=reply_markup,
        )
    else:
        await mailing_service.send_media_group(
            chat_ids=chat_ids,
            text=text,
            photo_file_ids=photo_file_ids
        )

    await callback_query.answer('Рассылка создана', show_alert=True)
    await callback_query.message.delete_reply_markup()
    view = AdminMenuView(config.web_app_base_url)
    await answer_view(callback_query.message, view)
