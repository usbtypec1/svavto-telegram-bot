from exceptions import InvalidNumberError

__all__ = ('parse_integer_number',)


def parse_integer_number(number: str) -> int:
    try:
        return int(number)
    except ValueError:
        raise InvalidNumberError(number=number)
