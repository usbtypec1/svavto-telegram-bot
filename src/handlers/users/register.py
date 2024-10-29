from aiogram import Router, F
from aiogram.filters import ExceptionTypeFilter, StateFilter
from aiogram.types import ErrorEvent, Message
from fast_depends import Depends, inject

from config import Config
from dependencies.repositories import get_staff_repository
from exceptions import StaffRegisterTextParseError, StaffAlreadyExistsError, \
    StaffNotFoundError
from models import StaffToRegister
from repositories import StaffRepository
from services import NotificationService
from services.telegram_events import answer_appropriate_event

__all__ = ('router',)

from views.button_texts import ButtonText

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(StaffAlreadyExistsError))
async def on_staff_already_exists_error(event: ErrorEvent) -> None:
    text = 'Сотрудник уже зарегистрирован'
    await answer_appropriate_event(event, text)


@router.error(ExceptionTypeFilter(StaffRegisterTextParseError))
async def on_staff_register_text_parse_error(event: ErrorEvent) -> None:
    text = (
        'Ошибка в форме заявки на регистрацию.'
        ' Попросите пользователя отправить заявку снова'
    )
    await answer_appropriate_event(event, text)


@router.message(
    F.web_app_data.button_text == ButtonText.REGISTER,
    StateFilter('*'),
)
@inject
async def on_register_form_filled(
        message: Message,
        notification_service: NotificationService,
        config: Config,
        staff_repository: StaffRepository = Depends(
            dependency=get_staff_repository,
            use_cache=False,
        ),
) -> None:
    try:
        await staff_repository.get_by_id(message.from_user.id)
    except StaffNotFoundError:
        staff = StaffToRegister.model_validate_json(message.web_app_data.data)
        await notification_service.send_new_user_notification(
            admin_user_ids=config.admin_user_ids,
            staff=staff,
            staff_id=message.from_user.id,
        )
        await message.answer(
            '✅ Ваша заявка на регистрацию отправлена на проверку',
        )
    else:
        await message.answer('❗️ Вы уже зарегистрированы')
