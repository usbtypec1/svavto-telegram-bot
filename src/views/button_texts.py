from enum import StrEnum

__all__ = ('ButtonText',)


class ButtonText(StrEnum):
    STAFF_LIST = '👥 Список всех сотрудников'
    SHIFTS = '📅 Графики'
    REPORTS = '📊 Отчеты'
    SHIFTS_TODAY = '📅 Сегодня в смене'
    CAR_WASH_LIST = '🚿 Меню моек'
    PENALTY = '🛑 Штрафануть'
    SURCHARGE = '💰 Доплатить'
    STAFF_PERFORMANCE = '📊 Кто сколько'
    UNDERFILLING = '💧 Недоливы'
    MAILING = '📩 Рассылка'
    SHIFT_START = '🚀 Начать смену'
    SHIFT_START_EXTRA = '🚀 Начать доп.смену'
    SHIFT_SCHEDULE = '📅 График работы'
    REPORT_FOR_PERIOD = '📊 Отчет за период'
    SHIFT_ADD_CAR = '🚗 Добавить автомобиль'
