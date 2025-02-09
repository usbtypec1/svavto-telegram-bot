from aiogram import Bot, F, Router
from aiogram.filters import ExceptionTypeFilter, StateFilter
from aiogram.types import ErrorEvent, Message, ReplyKeyboardRemove
from fast_depends import inject

from config import Config
from dependencies.repositories import StaffRepositoryDependency
from exceptions import StaffAlreadyExistsError
from models import StaffRegisterRequestData
from services.notifications import SpecificChatsNotificationService
from services.telegram_events import answer_appropriate_event
from ui.views import ButtonText, StaffRegisterRequestNotificationView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.web_app_data.button_text == ButtonText.REGISTER,
    StateFilter('*'),
)
@inject
async def on_register_form_filled(
        message: Message,
        admin_user_ids: set[int],
        bot: Bot,
        config: Config,
        staff_repository: StaffRepositoryDependency,
) -> None:
    admins_notification_service = SpecificChatsNotificationService(
        bot=bot,
        chat_ids=admin_user_ids,
    )
    request_data = StaffRegisterRequestData.model_validate_json(
        message.web_app_data.data,
    )
    try:
        await staff_repository.create_register_request(
            staff_id=message.from_user.id,
            full_name=request_data.full_name,
            car_sharing_phone_number=request_data.car_sharing_phone_number,
            console_phone_number=request_data.console_phone_number,
        )
    except StaffAlreadyExistsError:
        await message.answer('❗️ Вы уже зарегистрированы')
    else:
        await message.answer(
            '✅ Ваша заявка на регистрацию отправлена на проверку',
            reply_markup=ReplyKeyboardRemove(),
        )
        view = StaffRegisterRequestNotificationView(config.web_app_base_url)
        await admins_notification_service.send_view(view=view)
