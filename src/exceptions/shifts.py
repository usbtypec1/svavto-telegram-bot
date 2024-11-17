class StaffHasNoActiveShiftError(Exception):
    pass


class ShiftNotConfirmedError(Exception):
    pass


class StaffHasActiveShiftError(Exception):
    pass


class ShiftAlreadyFinishedError(Exception):
    pass


class ShiftAlreadyConfirmedError(Exception):
    pass


class StaffHasNoAnyShiftError(Exception):
    pass


class ShiftNotFoundError(Exception):
    pass


class CarAlreadyWashedOnShiftError(Exception):
    pass


class ShiftAlreadyExistsError(Exception):
    pass
