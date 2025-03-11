from enum import StrEnum, auto


__all__ = ('CallbackDataPrefix',)


class CallbackDataPrefix(StrEnum):
    CAR_WASH_DETAIL = auto()
    CAR_WASH_LIST = auto()
    CAR_WASH_CREATE = auto()
    CAR_WASH_CREATE_CONFIRM = auto()
    CAR_WASH_UPDATE = auto()
    CAR_WASH_UPDATE_CONFIRM = auto()
    CAR_WASH_DELETE_CONFIRM = auto()
    CAR_DETAIL_FOR_ADDITIONAL_SERVICES = auto()
    STAFF_DETAIL = auto()
    STAFF_UPDATE = auto()
    STAFF_LIST = auto()
    STAFF_MENU = auto()
    SHIFT_WORK_TYPE = auto()
    SHIFT_CAR_WASH_UPDATE = auto()
    SHIFT_CONFIRM = auto()
    SHIFT_REJECT = auto()
    SHIFT_FINISH_FLOW_START_ACCEPT = auto()
    SHIFT_FINISH_FLOW_START_REJECT = auto()
    SHIFT_FINISH_ACCEPT = auto()
    SHIFT_FINISH_REJECT = auto()
    SHIFT_FINISH_PHOTO_DELETE = auto()
    SHIFT_FINISH_PHOTO_NEXT_STEP = auto()
    SHIFT_REGULAR_START_ACCEPT = auto()
    SHIFT_REGULAR_START_REJECT = auto()
    SHIFT_START_CAR_WASH = auto()
    SHIFT_APPLY = auto()
    SHIFT_EXTRA_CREATE_ACCEPT = auto()
    SHIFT_EXTRA_CREATE_REJECT = auto()
    SHIFT_MONTH_CHOOSE = auto()
    MAILING = auto()
    MAILING_CREATE_ACCEPT = auto()
    MAILING_CREATE_REJECT = auto()
    MAILING_PHOTO_ACCEPT_FINISH = auto()
    SHIFT_START_REQUEST = auto()
    SHIFT_START_REQUEST_ACCEPT = auto()
    SHIFT_START_REQUEST_REJECT = auto()
    TEST_SHIFT_START = auto()
    SKIP = auto()
    SCHEDULED_SHIFT_START_ACCEPT = auto()
    SCHEDULED_SHIFT_START_REJECT = auto()
    SUPERVISION_DEAD_SOULS = auto()
    CAR_NUMBER_INPUT = auto()
    DRY_CLEANING_REQUEST_PHOTO_DELETE = auto()
    DRY_CLEANING_REQUEST_CONFIRM = auto()
    DRY_CLEANING_REQUEST_REJECT = auto()
