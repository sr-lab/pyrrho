import sys


def is_arg_passed (name):
    """ Returns true if an argument was passed, or false otherwise.
    Args:
        name (str): The name of the argument.
    Returns:
        str: True if a the argument was passed, or false otherwise.
    """
    arg = '-' + name
    return arg in sys.argv


def get_valued_arg (name):
    """ Returns the value of a valued argument, or none if that argument was not passed.
    Args:
        name (str): The name of the argument.
    Returns:
        str: The value of the argument, or none if it was not passed.
    """
    arg = '-' + name
    out = None
    if is_arg_passed(name):
        i = sys.argv.index(arg)
        if len(sys.argv) > i:
            out = sys.argv[i + 1]
    return out


def get_int_valued_arg (name):
    """ Returns the value of a valued argument as an integer, or none if that argument was not passed.
    Args:
        name (str): The name of the argument.
    Returns:
        str: The value of the argument as an integer, or none if it was not passed.
    """
    value = get_valued_arg(name)
    if not value is None:
        value = int(value)
    return value


def split_multi_arg (arg, delim=';'):
    """ Splits a multi-arg string along its delimiter (';' by default).
    Args:
        arg (str): The argument.
        delim (char): The delimited (';' by default).
    Returns:
        list of str: The split argument.
    """
    return arg.split(delim)
