from enum import IntEnum


class DryCleaningRequestStatus(IntEnum):
    PENDING = 1
    APPROVED = 2
    REJECTED = 3
