from aiogram import F, Router
from aiogram.filters import (
    CommandStart, ExceptionTypeFilter, StateFilter, invert_f, or_f,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent, Message
from fast_depends import Depends, inject

from config import Config
from dependencies.repositories import get_shift_repository
from exceptions import StaffHasNoActiveShiftError, StaffNotFoundError
from filters import admins_filter
from models import Staff
from repositories import ShiftRepository
from views.admins import AdminMenuView
from views.base import answer_view
from views.button_texts import ButtonText
from views.menu import MainMenuView, RegisterView, ShiftMenuView

__all__ = ('router',)

from views.register import StaffRegisterView

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(StaffNotFoundError))
async def on_performer_not_found_error(event: ErrorEvent) -> None:
    view = RegisterView()
    if event.update.message is not None:
        await answer_view(event.update.message, view)
    elif event.update.callback_query is not None:
        await answer_view(event.update.callback_query.message, view)
    else:
        raise event.exception


@router.message(
    or_f(
        CommandStart(),
        F.text == ButtonText.MAIN_MENU,
    ),
    invert_f(admins_filter),
    StateFilter('*'),
)
@inject
async def on_show_menu(
        message: Message,
        config: Config,
        state: FSMContext,
        staff: Staff | None,
        shift_repository: ShiftRepository = Depends(
            get_shift_repository,
            use_cache=False,
        ),
) -> None:
    await state.clear()
    if staff is None:
        view = StaffRegisterView(config.web_app_base_url)
    else:
        try:
            await shift_repository.get_active(message.from_user.id)
        except StaffHasNoActiveShiftError:
            view = MainMenuView(config.web_app_base_url)
        else:
            view = ShiftMenuView(
                staff_id=message.from_user.id,
                web_app_base_url=config.web_app_base_url,
            )
    await answer_view(message, view)


@router.message(
    or_f(
        CommandStart(),
        F.text == ButtonText.MAIN_MENU,
    ),
    admins_filter,
    StateFilter('*'),
)
@inject
async def on_show_admin_menu(
        message: Message,
        config: Config,
        state: FSMContext,
) -> None:
    await state.clear()
    view = AdminMenuView(config.web_app_base_url)
    await answer_view(message, view)
