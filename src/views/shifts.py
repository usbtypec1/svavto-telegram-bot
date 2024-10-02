from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_data import ShiftWorkTypeChoiceCallbackData
from enums import ShiftWorkType
from views.base import TextView

__all__ = ('ShiftWorkTypeChoiceView', 'shift_work_types_and_names')

shift_work_types_and_names: tuple[tuple[ShiftWorkType, str], ...] = (
    (ShiftWorkType.MOVE_TO_WASH, 'Перегон ТС на мойку'),
    (ShiftWorkType.LIGHT_WASHES, 'Легкие мойки'),
    (ShiftWorkType.FIND_VEHICLE_IN_CITY, 'Поиск ТС в городе'),
    (ShiftWorkType.ASSIGNMENT_MOVE, 'Перегон по заданию'),
)


class ShiftWorkTypeChoiceView(TextView):
    text = 'Выберите направление, в котором хотите начать смену:'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=shift_work_type_name,
                    callback_data=ShiftWorkTypeChoiceCallbackData(
                        work_type=shift_work_type,
                    ).pack(),
                )
            ]
            for shift_work_type, shift_work_type_name in
            shift_work_types_and_names
        ]
    )
