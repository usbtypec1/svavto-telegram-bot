class StaffHasNoActiveShiftError(Exception):
    pass


class ShiftByDateNotFoundError(Exception):
    pass


class ShiftNotConfirmedError(Exception):
    pass


class StaffHasActiveShiftError(Exception):
    pass


class ShiftAlreadyFinishedError(Exception):
    pass


class ShiftAlreadyConfirmedError(Exception):
    pass
