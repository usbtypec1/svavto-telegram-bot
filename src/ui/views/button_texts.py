from enum import StrEnum


__all__ = ('ButtonText',)


class ButtonText(StrEnum):
    STAFF_LIST = '👥 Список сотрудников'
    STAFF_REGISTER_REQUESTS = '🚀 Запросы на регистрацию'
    SHIFTS_ADMIN_MENU = '📅 Графики'
    SHIFTS_FOR_SPECIFIC_DATE = '📅 Сегодня в смене'
    CAR_WASH_LIST = '🚿 Меню моек'
    PENALTY_CREATE_MENU = '🛑 Оштрафовать'
    PENALTY_CREATE_CAR_WASH = '🛑 Оштрафовать мойку'
    PENALTY_CREATE_CAR_TRANSPORTER = '🛑 Оштрафовать перегонщика'
    PENALTY_LIST = '🛑 Все мои штрафы'
    SURCHARGE_CREATE_MENU = '💰 Доплатить'
    SURCHARGE_CREATE_CAR_WASH = '💰 Доплатить мойке'
    SURCHARGE_CREATE_CAR_TRANSPORTER = '💰 Доплатить перегонщику'
    SURCHARGE_LIST = '💰 Все мои доплаты'
    SUPERVISION_MENU = '🔍 Контроль'
    SUPERVISION_CAR_TRANSFERS = '🚗 Добавленные авто'
    SUPERVISION_SHIFT_CONFIRMATIONS = '📝 Подтверждения смен'
    SUPERVISION_STAFF_WITHOUT_SHIFTS = '😶‍🌫️ Мертвые души'
    SHIFT_CARS_WITHOUT_WINDSHIELD_WASHER = '💧 Недоливы'
    MAILING = '📩 Рассылка'
    SHIFT_START = '🚀 Начать смену'
    SHIFT_START_EXTRA = '🚀 Запросить доп.смену'
    SHIFT_SCHEDULE = '📅 График работы'
    REPORT_FOR_PERIOD = '📊 Отчет за период'
    SHIFT_ADD_CAR = '🚗 Добавить автомобиль'
    SHIFT_ADDITIONAL_SERVICES = '🔧 Отметить доп.услуги'
    SHIFT_ADDED_CARS = '🚗 Добавленные автомобили'
    SHIFT_CHANGE_CAR_WASH = '🫧 Поменять мойку'
    SHIFT_END = '🛑 Завершить смену'
    SHIFT_DRY_CLEANING_REQUEST = '🫧 Запросить химчистку'
    ATTACH_REPLY_MARKUP = '⌨ Привязать кнопки'
    SKIP = '➡ Пропустить'
    MAILING_STAFF = '👥 Выбрать сотрудников'
    REGISTER = '🚀 Зарегистрироваться'
    MAIN_MENU = '📲 Главное меню'
    SHIFT_MONTH_LIST = '📆 Мой график'
    CAR_ADDITIONAL_SERVICES = '🔧 Отметить доп.услуги авто'
    LATER = '➡ Сделаю это позже'
    SHIFT_APPLY = '✏️ Записаться на смены'
    SHIFT_SCHEDULE_MONTH_CALENDAR = '📅 Выбрать даты рабочих смен'
    EXTRA_SHIFT_CALENDAR = '📆 Выбрать дату на доп.смену'
    OTHER = '📱 Другое'
    TEST_SHIFT_REQUEST = '📅 Выдать тестовый доступ'
    REPORTS = '📊 Отчеты'
    SPECIFIC_SHIFT = '📝 Открыть список смен'
    SHIFT_FINISH_CHECK = '🔍 Проверить'
    DRY_CLEANING_REQUEST_PHOTO_INPUT_FINISH = '🔜 Следующий шаг'
    DRY_CLEANING_REQUEST_SERVICES = '🫧 Выбрать услуги'
