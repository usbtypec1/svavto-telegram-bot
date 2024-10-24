from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import (
    PenaltyCreateChooseStaffCallbackData,
    PenaltyCreateChooseReasonCallbackData,
)
from callback_data.prefixes import CallbackDataPrefix
from enums import PenaltyReason
from models import Staff, Penalty
from views.base import TextView

__all__ = (
    'PenaltyCreateChooseStaffView',
    'PenaltyCreateChooseReasonView',
    'PenaltyCreateInputOtherReasonView',
    'PenaltyCreateConfirmView',
    'PenaltyCreateSuccessView',
)


class PenaltyCreateChooseStaffView(TextView):

    def __init__(self, staff_list: Iterable[Staff]):
        self.__staff_list = tuple(staff_list)

    def get_text(self) -> str:
        if not self.__staff_list:
            return 'Некого штрафовать'
        return 'Выберите Сотрудника'

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
    text = 'Выберите причину штрафа из списка'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Невыход',
                    callback_data=PenaltyCreateChooseReasonCallbackData(
                        reason=PenaltyReason.NOT_SHOWING_UP,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Ранний уход',
                    callback_data=PenaltyCreateChooseReasonCallbackData(
                        reason=PenaltyReason.EARLY_LEAVE,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Отчет не вовремя',
                    callback_data=PenaltyCreateChooseReasonCallbackData(
                        reason=PenaltyReason.LATE_REPORT,
                    ).pack(),
                ),
            ]
        ],
    )


class PenaltyCreateInputOtherReasonView(TextView):
    text = 'Вы можете сами ввести причину'
    reply_markup = ForceReply(input_field_placeholder='Другая причина')


class PenaltyCreateConfirmView(TextView):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Да',
                    callback_data=CallbackDataPrefix.PENALTY_CREATE_ACCEPT,
                ),
                InlineKeyboardButton(
                    text='Нет',
                    callback_data=CallbackDataPrefix.PENALTY_CREATE_REJECT,
                ),
            ],
        ],
    )

    def __init__(self, staff: Staff, reason: str):
        self.__staff = staff
        self.__reason = reason

    def get_text(self) -> str:
        return (
            '❗️ Вы действительно хотите оштрафовать'
            f' сотрудника {self.__staff.full_name}'
            f' по причине <i>{self.__reason}</i>?'
        )


class PenaltyCreateSuccessView(TextView):

    def __init__(self, penalty: Penalty, staff: Staff):
        self.__penalty = penalty
        self.__staff = staff

    def get_text(self) -> str:
        if self.__penalty.is_notification_delivered:
            notification_delivered_line = '✅ Уведомление отправлено'
        else:
            notification_delivered_line = '❌ Уведомление не отправлено'
        return (
            f'❗️ Сотрудник {self.__staff.full_name} оштрафован'
            f' по причине <i>{self.__penalty.reason}</i>\n'
            f'{notification_delivered_line}'
        )
