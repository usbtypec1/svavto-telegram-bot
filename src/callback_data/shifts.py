from aiogram.filters.callback_data import CallbackData

from callback_data.prefixes import CallbackDataPrefix
from enums import ShiftWorkType

__all__ = (
    'ShiftWorkTypeChoiceCallbackData',
    'ShiftCarWashUpdateCallbackData',
    'ShiftRejectCallbackData',
    'ShiftStartCallbackData',
    'ShiftStartCarWashCallbackData',
    'ShiftApplyCallbackData',
    'ExtraShiftCreateAcceptCallbackData',
    'ExtraShiftCreateRejectCallbackData',
    'ExtraShiftStartCallbackData',
    'ShiftStartRequestAcceptCallbackData',
    'ShiftStartRequestRejectCallbackData',
    'ShiftImmediateStartCallbackData',
    'ScheduledShiftStartAcceptCallbackData',
    'ScheduledShiftStartRejectCallbackData',
)


class ShiftWorkTypeChoiceCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SHIFT_WORK_TYPE,
):
    work_type: ShiftWorkType


class ShiftCarWashUpdateCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SHIFT_CAR_WASH_UPDATE,
):
    car_wash_id: int


class ShiftStartCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SHIFT_START_ACCEPT,
):
    shift_id: int


class ShiftRejectCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SHIFT_FINISH_REJECT,
):
    shift_id: int


class ShiftStartCarWashCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SHIFT_START_CAR_WASH,
):
    car_wash_id: int


class ShiftApplyCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SHIFT_APPLY,
):
    month: int
    year: int


class ExtraShiftCreateAcceptCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SHIFT_EXTRA_CREATE_ACCEPT,
):
    staff_id: int
    date: str


class ExtraShiftCreateRejectCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SHIFT_EXTRA_CREATE_REJECT,
):
    staff_id: int
    date: str


class ExtraShiftStartCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SHIFT_EXTRA_START,
):
    date: str


class ShiftStartRequestAcceptCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SHIFT_START_REQUEST_ACCEPT,
):
    shift_id: int


class ShiftStartRequestRejectCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SHIFT_START_REQUEST_REJECT,
):
    shift_id: int


class ShiftImmediateStartCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SHIFT_IMMEDIATE_START,
):
    date: str


class ScheduledShiftStartAcceptCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SCHEDULED_SHIFT_START_ACCEPT,
):
    shift_id: int


class ScheduledShiftStartRejectCallbackData(
    CallbackData,
    prefix=CallbackDataPrefix.SCHEDULED_SHIFT_START_REJECT,
):
    shift_id: int
