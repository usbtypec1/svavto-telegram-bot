from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fast_depends import Depends, inject

from callback_data.prefixes import CallbackDataPrefix
from config import Config
from dependencies.repositories import get_staff_repository
from enums import MailingType, StaffOrderBy
from filters import admins_filter
from models import MailingParams
from repositories import StaffRepository
from services.mailing import (
    filter_banned_staff,
    filter_last_active_staff,
    filter_staff_by_chat_ids,
)
from services.notifications import MailingService
from states import MailingStates
from ui.views import AdminMenuView, edit_as_accepted
from ui.views import answer_text_view

__all__ = ('router',)

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
        mailing_service: MailingService,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    state_data: dict = await state.get_data()
    await state.clear()
    mailing_params = MailingParams.model_validate(state_data)

    staff_list = await staff_repository.get_all(
        order_by=StaffOrderBy.LAST_ACTIVITY_AT_DESC,
        include_banned=False,
        limit=1000,
    )
    staff_list = filter_banned_staff(staff_list.staff)

    if mailing_params.type == MailingType.SPECIFIC_STAFF:
        staff_list = filter_staff_by_chat_ids(
            staff_list=staff_list,
            chat_ids=mailing_params.chat_ids,
        )
    elif mailing_params.type == MailingType.LAST_ACTIVE:
        staff_list = filter_last_active_staff(
            staff_list=staff_list,
            last_activity_days=30,
        )

    chat_ids = [staff.id for staff in staff_list]

    await callback_query.answer('Рассылка создана', show_alert=True)

    if len(mailing_params.photo_file_ids) == 0:
        await mailing_service.send_text(
            chat_ids=chat_ids,
            text=mailing_params.text,
            reply_markup=mailing_params.reply_markup,
        )
    elif len(mailing_params.photo_file_ids) == 1:
        await mailing_service.send_single_photo(
            chat_ids=chat_ids,
            text=mailing_params.text,
            photo_file_id=mailing_params.photo_file_ids[0],
            reply_markup=mailing_params.reply_markup,
        )
    else:
        await mailing_service.send_media_group(
            chat_ids=chat_ids,
            text=mailing_params.text,
            photo_file_ids=mailing_params.photo_file_ids
        )

    await callback_query.message.answer('✅ Рассылка завершена')
    await edit_as_accepted(callback_query.message)
    view = AdminMenuView(config.web_app_base_url)
    await answer_text_view(callback_query.message, view)
