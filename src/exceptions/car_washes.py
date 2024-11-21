class CarWashNotFoundError(Exception):
    pass


class CarWashSameAsCurrentError(Exception):
    """Raised when trying to set the same car wash as current."""


class AdditionalServicesCouldNotBeProvidedError(Exception):

    def __init__(self, *args, service_ids: list[str]):
        super().__init__(*args)
        self.service_ids = service_ids
