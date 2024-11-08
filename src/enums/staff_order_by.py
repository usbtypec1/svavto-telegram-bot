from enum import StrEnum

__all__ = ('StaffOrderBy',)


class StaffOrderBy(StrEnum):
    FULL_NAME_ASC = 'full_name'
    FULL_NAME_DESC = '-full_name'
    LAST_ACTIVITY_AT_ASC = 'last_activity_at'
    LAST_ACTIVITY_AT_DESC = '-last_activity_at'
    CREATED_AT_ASC = 'created_at'
    CREATED_AT_DESC = '-created_at'
