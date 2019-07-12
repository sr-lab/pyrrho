import re


def is_symbol (c):
    """ Checks whether a character is a symbol.

    A symbol is defined as any character that is neither a lowercase letter, uppercase letter or digit.

    Args:
        c (char): The character to check.

    Returns:
        bool: True if the character is a symbol, otherwise false.
    """
    return (not c.islower() and not c.isupper() and not c.isdigit())


def count_lowers (val):
    """ Counts the number of lowercase letters in a string.

    Args:
        val (str): The string to count lowercase letters in.

    Returns:
        int: The number of lowercase letters in the string.
    """
    return sum(1 for c in val if c.islower())


def count_uppers (val):
    """ Counts the number of uppercase letters in a string.

    Args:
        val (str): The string to count uppercase letters in.

    Returns:
        int: The number of uppercase letters in the string.
    """
    return sum(1 for c in val if c.isupper())


def count_letters (val):
    """ Counts the number of letters in a string.

    Args:
        val (str): The string to count letters in.

    Returns:
        int: The number of letters in the string.
    """
    return sum(1 for c in val if c.isalpha())


def count_digits (val):
    """ Counts the number of digits in a string.

    Args:
        val (str): The string to count digits in.

    Returns:
        int: The number of digits in the string.
    """
    return sum(1 for c in val if c.isdigit())


def count_symbols (val):
    """ Counts the number of symbols in a string.

    A symbol is defined as any character that is neither a lowercase letter, uppercase letter or digit.

    Args:
        val (str): The string to count symbols in.

    Returns:
        int: The number of symbols in the string.
    """
    return sum(1 for c in val if is_symbol(c))


def count_words (val):
    """ Counts the number of words in a string.

    A word is defined as a sequence of one or more letters separated by one or more non-letter characters.

    Args:
        val (str): The string to count words in.

    Returns:
        int: The number of words in the string.
    """
    current = 0
    count = 0
    in_word = False
    while current < len(val):
        if not in_word and val[current].isalpha():
            in_word = True
            count += 1
        elif in_word and not val[current].isalpha():
            in_word = False
        current += 1
    return count


def count_classes (val):
    """ Counts the number of character classes present in the string.

    Character classes consist of uppercase, lowercase, digits and symbols.

    Args:
        val (str): The string to count character classes in.

    Returns:
        int: The number of words in the string.
    """
    total = 0
    if count_lowers(val) > 0:
        total += 1
    if count_uppers(val) > 0:
        total += 1
    if count_digits(val) > 0:
        total += 1
    if count_symbols(val) > 0:
        total += 1
    return total


def contains_rep (val):
    """ Checks whether or not a string contains repeated characters.

    Args:
        val (str): The string to check for repetitions.

    Returns:
        bool: True if the string contains repetitions, otherwise false.
    """
    current = 0
    while current < len(val) - 1:
        if val[current] == val[current + 1]:
            return True
        current += 1
    return False


def contains_consec (val):
    """ Checks whether or not a string contains adjacent characters with consecutive code points.

    Args:
        val (str): The string to check for consecutive characters.

    Returns:
        bool: True if the string has consecutive characters, otherwise false.
    """
    current = 0
    while current < len(val) - 1:
        if ord(val[current]) == ord(val[current + 1]) + 1 or ord(val[current]) == ord(val[current + 1]) - 1:
            return True
        current += 1
    return False


def strip_non_lowers (val):
    """ Strips all non-lowercase characters from a string.

    Args:
        val (str): The string to strip non-lowercase characters from.

    Returns:
        str: The string with all non-lowercase characters stripped from it.
    """
    buffer = ""
    for char in val:
        if char.islower():
            buffer += char
    return buffer


def dict_normalise (val):
    """ Converts a string to lowercase and strips all non-letter characters.

    Args:
        val (str): The string to convert to to lowercase and strip all non-letter characters from.

    Returns:
        str: The string converted to lowercase with all non-letter characters stripped from it.
    """
    return strip_non_lowers(val.lower())
