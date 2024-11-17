class InvalidNumberError(Exception):

    def __init__(self, *args, number: str):
        self.number = number
        super().__init__(args)
