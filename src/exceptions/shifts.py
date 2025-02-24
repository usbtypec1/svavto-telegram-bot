import datetime


class StaffHasNoActiveShiftError(Exception):
    pass


class ShiftNotConfirmedError(Exception):
    pass


class StaffHasActiveShiftError(Exception):
    pass


class ShiftAlreadyFinishedError(Exception):

    def __init__(self, message: str, shift_date: datetime.date):
        super().__init__(message)
        self.shift_date = shift_date


class ShiftAlreadyConfirmedError(Exception):
    pass


class StaffHasNoAnyShiftError(Exception):
    pass


class ShiftNotFoundError(Exception):
    pass


class CarAlreadyWashedOnShiftError(Exception):
    pass


class ShiftAlreadyExistsError(Exception):

    def __init__(self, message, conflict_dates: list[str]) -> None:
        super().__init__(message)
        self.conflict_dates = [
            datetime.date.fromisoformat(date)
            for date in conflict_dates
        ]


class ShiftFinishPhotosCountExceededError(Exception):
    pass


class ShiftDateExpiredError(Exception):

    def __init__(self, shift_date: datetime.date) -> None:
        super().__init__()
        self.shift_date = shift_date


class ShiftDateHasNotComeError(Exception):

    def __init__(self, shift_date: datetime.date) -> None:
        super().__init__()
        self.shift_date = shift_date


class InvalidTimeToStartShiftError(Exception):
    pass
