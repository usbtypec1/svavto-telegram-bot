class CarWashNotFoundError(Exception):
    pass


class CarWashSameAsCurrentError(Exception):
    """Raised when trying to set the same car wash as current."""
