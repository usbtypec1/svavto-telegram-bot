from collections.abc import Iterable
from typing import Final

from aiogram.types import (
    ForceReply, InlineKeyboardButton,
    InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

import ui.texts
from callback_data import (
    PenaltyCreateChooseReasonCallbackData,
    PenaltyCreateChooseStaffCallbackData,
)
from callback_data.prefixes import CallbackDataPrefix
from enums import PenaltyConsequence, PenaltyReason
from models import Penalty, Staff
from ui.markups import create_confirm_reject_markup
from ui.views import ButtonText
from ui.views.base import PhotoView, TextView


__all__ = (
    'PenaltyCreateChooseStaffView',
    'PenaltyCreateChooseReasonView',
    'PenaltyCreateInputOtherReasonView',
    'PenaltyCreateConfirmView',
    'PenaltyCreateSuccessView',
    'PenaltyPhotoInputView',
    'penalty_reason_to_name',
    'PenaltyCreateNotificationView',
    'PhotoCreateWithPhotoNotificationView',
    'format_penalty_create_notification_text',
    'PenaltyCreateMenuView',
)

penalty_reason_to_name: Final[dict[PenaltyReason: str]] = {
    PenaltyReason.NOT_SHOWING_UP: '🙅 Невыход',
    PenaltyReason.EARLY_LEAVE: '🏃 Ранний уход',
    PenaltyReason.LATE_REPORT: '📝 Отчет не вовремя',
    PenaltyReason.OTHER: '✏️ Другая причина',
}


class PenaltyCreateInputOtherReasonView(TextView):
    text = 'Вы можете сами ввести причину'
    reply_markup = ForceReply(input_field_placeholder='Другая причина')


class PenaltyCreateConfirmView(TextView):
    reply_markup = create_confirm_reject_markup(
        confirm_callback_data=CallbackDataPrefix.PENALTY_CREATE_ACCEPT,
        reject_callback_data=CallbackDataPrefix.PENALTY_CREATE_REJECT,
    )

    def __init__(
            self,
            *,
            staff: Staff,
            reason: str,
            amount: int | None,
    ):
        self.__staff = staff
        self.__reason = reason
        self.__amount = amount

    def get_text(self) -> str:
        if self.__amount is not None:
            return (
                '❗️ Вы действительно хотите оштрафовать'
                f' сотрудника {self.__staff.full_name}'
                f' на сумму {self.__amount} по причине <i>{self.__reason}</i>?'
            )
        return (
            '❗️ Вы действительно хотите оштрафовать'
            f' сотрудника {self.__staff.full_name}'
            f' по причине <i>{self.__reason}</i>?'
        )


class PenaltyCreateChooseStaffView(TextView):

    def __init__(self, staff_list: Iterable[Staff]):
        self.__staff_list = tuple(staff_list)

    def get_text(self) -> str:
        if not self.__staff_list:
            return ui.texts.NO_ANY_STAFF
        return '👥 Выберите сотрудника которого хотите оштрафовать'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        keyboard.max_width = 1

        for staff in self.__staff_list:
            keyboard.button(
                text=staff.full_name,
                callback_data=PenaltyCreateChooseStaffCallbackData(
                    staff_id=staff.id,
                ),
            )

        return keyboard.as_markup()


class PenaltyCreateChooseReasonView(TextView):
    text = '✏️ Выберите причину штрафа из списка'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=reason_name,
                    callback_data=PenaltyCreateChooseReasonCallbackData(
                        reason=reason,
                    ).pack(),
                )
            ] for reason, reason_name in penalty_reason_to_name.items()
        ],
    )


class PenaltyCreateSuccessView(TextView):

    def __init__(self, penalty: Penalty):
        self.__penalty = penalty

    def get_text(self) -> str:
        reason_name = penalty_reason_to_name.get(
            self.__penalty.reason,
            self.__penalty.reason,
        )
        text = (
            f'❗️ Сотрудник {self.__penalty.staff_full_name} оштрафован'
            f'\nПричина: {reason_name}'
            f'\nСумма: {self.__penalty.amount}'
        )
        if self.__penalty.consequence == PenaltyConsequence.DISMISSAL:
            text += '\n❗️ Сотрудник должен быть уволен'
        if self.__penalty.consequence == PenaltyConsequence.WARN:
            text += '\n❗️ Сотруднику отправлено предупреждение'
        return text


class PenaltyPhotoInputView(TextView):
    text = '🖼️ Вы можете прикрепить фото'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='➡️ Пропустить',
                    callback_data=CallbackDataPrefix.SKIP,
                ),
            ],
        ],
    )


def format_penalty_create_notification_text(penalty: Penalty) -> str:
    reason_name = penalty_reason_to_name.get(
        penalty.reason,
        penalty.reason,
    )
    return (
        f'❗️ {penalty.staff_full_name}, вы получили новый штраф'
        f'\nПричина: {reason_name}'
        f'\nСумма: {penalty.amount}'
    )


class PenaltyCreateNotificationView(TextView):

    def __init__(self, *, penalty: Penalty, web_app_base_url: str):
        self.__penalty = penalty
        self.__web_app_base_url = web_app_base_url

    def get_text(self) -> str:
        return format_penalty_create_notification_text(self.__penalty)


class PhotoCreateWithPhotoNotificationView(PhotoView):

    def __init__(
            self,
            *,
            penalty: Penalty,
            web_app_base_url: str,
            photo_file_id: str,
    ):
        self.__penalty = penalty
        self.__web_app_base_url = web_app_base_url
        self.__photo_file_id = photo_file_id

    def get_caption(self) -> str:
        return format_penalty_create_notification_text(self.__penalty)

    def get_photo(self) -> str:
        return self.__photo_file_id


class PenaltyCreateMenuView(TextView):
    text = '🛑 Меню штрафов'

    def __init__(self, *, web_app_base_url: str):
        self.__web_app_base_url = web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        car_transporter_penalties_web_app_url = (
            f'{self.__web_app_base_url}/penalties/car-transporters'
        )
        car_wash_penalties_web_app_url = (
            f'{self.__web_app_base_url}/penalties/car-wash'
        )
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(
                        text=ButtonText.PENALTY_CREATE_CAR_TRANSPORTER,
                        web_app=WebAppInfo(
                            url=car_transporter_penalties_web_app_url,
                        )
                    ),
                ],
                [
                    KeyboardButton(
                        text=ButtonText.PENALTY_CREATE_CAR_WASH,
                        web_app=WebAppInfo(
                            url=car_wash_penalties_web_app_url,
                        )
                    ),
                ],
                [
                    KeyboardButton(
                        text=ButtonText.MAIN_MENU,
                    ),
                ],
            ],
        )
