class StaffNotFoundError(Exception):
    pass


class StaffRegisterTextParseError(Exception):
    """Raised when register text could not be parsed properly."""


class StaffAlreadyExistsError(Exception):
    pass
