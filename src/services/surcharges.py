from exceptions.surcharges import SurchargeAmountParseError

__all__ = ('parse_money_amount',)


def parse_money_amount(text: str) -> int:
    """
    Parse money amount from text.

    Args:
        text: Text to parse money amount from.

    Returns:
        Money amount.

    Raises:
        SurchargeAmountParseError: If money amount can't be parsed from text.
    """
    try:
        return int(text.replace(' ', ''))
    except ValueError:
        raise SurchargeAmountParseError
