from collections.abc import Iterable
from typing import Final

from aiogram.types import (
    ForceReply, InlineKeyboardButton,
    InlineKeyboardMarkup, WebAppInfo,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import (
    PenaltyCreateChooseReasonCallbackData,
    PenaltyCreateChooseStaffCallbackData,
)
from callback_data.prefixes import CallbackDataPrefix
from enums import PenaltyConsequence, PenaltyReason
from models import Penalty, Staff
from views.base import TextView

__all__ = (
    'PenaltyCreateChooseStaffView',
    'PenaltyCreateChooseReasonView',
    'PenaltyCreateInputOtherReasonView',
    'PenaltyCreateConfirmView',
    'PenaltyCreateSuccessView',
    'PenaltyPhotoInputView',
    'penalty_reason_to_name',
    'PenaltyCreateNotificationView',
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
    __accept_button = InlineKeyboardButton(
        text='✅ Да',
        callback_data=CallbackDataPrefix.PENALTY_CREATE_ACCEPT,
    )
    __reject_button = InlineKeyboardButton(
        text='❌ Нет',
        callback_data=CallbackDataPrefix.PENALTY_CREATE_REJECT,
    )
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[__accept_button, __reject_button]],
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
            return '😔 Некого штрафовать'
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

    def __init__(self, penalty: Penalty, staff: Staff):
        self.__penalty = penalty
        self.__staff = staff

    def get_text(self) -> str:
        reason_name = penalty_reason_to_name.get(
            self.__penalty.reason,
            self.__penalty.reason,
        )
        text = (
            f'❗️ Сотрудник {self.__staff.full_name} оштрафован'
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


class PenaltyCreateNotificationView(TextView):

    def __init__(self, penalty: Penalty, web_app_base_url: str):
        self.__penalty = penalty
        self.__web_app_base_url = web_app_base_url

    def get_text(self) -> str:
        reason_name = penalty_reason_to_name.get(
            self.__penalty.reason,
            self.__penalty.reason,
        )
        return (
            f'❗️ {self.__penalty.staff.full_name}, вы получили новый штраф'
            f'\nПричина: {reason_name}'
            f'\nСумма: {self.__penalty.amount}'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        url = f'{self.__web_app_base_url}/penalties/{self.__penalty.staff.id}'
        button = InlineKeyboardButton(
            text='🛑 Все мои штрафы',
            web_app=WebAppInfo(url=url),
        )
        return InlineKeyboardMarkup(inline_keyboard=[[button]])
