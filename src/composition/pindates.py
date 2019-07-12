from .charclass import count_digits


def is_valid_day (val):
    """ Checks whether or not a two-digit string is a valid date day.

    Args:
        val (str): The string to check.

    Returns:
        bool: True if the string is a valid date day, otherwise false.
    """
    if len(val) == 2 and count_digits(val) == 2:
        day = int(val)
        return day > 0 and day < 32
    return False


def is_valid_month (val):
    """ Checks whether or not a two-digit string is a valid date month.

    Args:
        val (str): The string to check.

    Returns:
        bool: True if the string is a valid date month, otherwise false.
    """
    if len(val) == 2 and count_digits(val) == 2:
        month = int(val)
        return month > 0 and month < 13
    return False


def is_ddmmyy (val):
    """ Checks whether or not a six-digit string is a valid ddmmyy date.

    Args:
        val (str): The string to check.

    Returns:
        bool: True if the string is a valid ddmmyy date, otherwise false.
    """
    if len(val) == 6 and count_digits(val) == 6:
        return is_valid_day(val[0:2]) and is_valid_month(val[2:4])
    return False


def is_mmddyy (val):
    """ Checks whether or not a six-digit string is a valid mmddyy date.

    Args:
        val (str): The string to check.

    Returns:
        bool: True if the string is a valid mmddyy date, otherwise false.
    """
    if len(val) == 6 and count_digits(val) == 6:
        return is_valid_day(val[2:4]) and is_valid_month(val[0:2])
    return False


def is_yymmdd (val):
    """ Checks whether or not a six-digit string is a valid yymmdd date.

    Args:
        val (str): The string to check.

    Returns:
        bool: True if the string is a valid yymmdd date, otherwise false.
    """
    if len(val) == 6 and count_digits(val) == 6:
        return is_valid_day(val[2:4]) and is_valid_month(val[4:6])
    return False


def is_date (val):
    """ Checks whether or not a six-digit string is a valid date.

    Args:
        val (str): The string to check.

    Returns:
        bool: True if the string is a valid date, otherwise false.
    """
    return is_ddmmyy(val) or is_mmddyy(val) or is_yymmdd(val)
