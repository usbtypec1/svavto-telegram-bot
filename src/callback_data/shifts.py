from aiogram.filters.callback_data import CallbackData

from enums import ShiftWorkType

__all__ = ('ShiftWorkTypeChoiceCallbackData',)


class ShiftWorkTypeChoiceCallbackData(CallbackData, prefix='shift-work-type'):
    work_type: ShiftWorkType
