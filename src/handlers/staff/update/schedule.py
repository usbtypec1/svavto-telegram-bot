from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from fast_depends import inject, Depends
from pydantic import TypeAdapter

from callback_data import StaffScheduleDetailCallbackData
from config import Config
from dependencies.repositories import get_staff_repository
from filters import admins_filter
from models import MonthAndYear, StaffAvailableDates
from repositories import StaffRepository
from views.admins import AdminMenuView
from views.base import answer_view
from views.button_texts import ButtonText
from views.schedules import StaffListForScheduleView, StaffScheduleDetailView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == ButtonText.SHIFTS,
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
    view = StaffListForScheduleView(staff_list)
    await answer_view(message, view)


@router.callback_query(
    StaffScheduleDetailCallbackData.filter(),
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_show_staff_detail(
        callback_query: CallbackQuery,
        callback_data: StaffScheduleDetailCallbackData,
        config: Config,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    staff = await staff_repository.get_by_id(callback_data.staff_id)
    view = StaffScheduleDetailView(staff, config.web_app_base_url)
    await answer_view(callback_query.message, view)


@router.message(
    F.web_app_data.button_text == ButtonText.AVAILABLE_DATES,
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_choose_staff_available_dates(
        message: Message,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    staff_available_dates = StaffAvailableDates.model_validate_json(
        message.web_app_data.data,
    )
    await staff_repository.update_available_dates(
        staff_available_dates=staff_available_dates,
    )
    await message.answer('Доступные месяцы обновлены')
    view = AdminMenuView()
    await answer_view(message, view)
