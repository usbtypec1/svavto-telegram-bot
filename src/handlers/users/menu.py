from aiogram import F, Router
from aiogram.filters import (
    CommandStart, ExceptionTypeFilter, StateFilter, invert_f, or_f,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ErrorEvent, Message
from fast_depends import Depends, inject

from callback_data.prefixes import CallbackDataPrefix
from config import Config
from dependencies.repositories import get_shift_repository
from exceptions import StaffHasNoActiveShiftError, StaffNotFoundError
from filters import admins_filter
from models import Staff
from repositories import ShiftRepository
from ui.views import AdminMenuView
from ui.views import answer_text_view
from ui.views import ButtonText
from ui.views import MainMenuView, RegisterView, ShiftMenuView

__all__ = ('router',)

from ui.views import StaffRegisterView

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(StaffNotFoundError))
async def on_performer_not_found_error(event: ErrorEvent) -> None:
    view = RegisterView()
    if event.update.message is not None:
        await answer_text_view(event.update.message, view)
    elif event.update.callback_query is not None:
        await answer_text_view(event.update.callback_query.message, view)
    else:
        raise event.exception


@router.callback_query(
    F.data == CallbackDataPrefix.STAFF_MENU,
    invert_f(admins_filter),
    StateFilter('*'),
)
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
        message_or_callback_query: Message | CallbackQuery,
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
            await shift_repository.get_active(
                message_or_callback_query.from_user.id,
            )
        except StaffHasNoActiveShiftError:
            view = MainMenuView(
                staff_id=message_or_callback_query.from_user.id,
                web_app_base_url=config.web_app_base_url,
            )
        else:
            view = ShiftMenuView(
                staff_id=message_or_callback_query.from_user.id,
                web_app_base_url=config.web_app_base_url,
            )
    if isinstance(message_or_callback_query, Message):
        await answer_text_view(message_or_callback_query, view)
    else:
        await answer_text_view(message_or_callback_query.message, view)
        await message_or_callback_query.message.delete()



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
    await answer_text_view(message, view)
