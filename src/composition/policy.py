import sys

from .charclass import *
from .pindates import *


""" Cached, loaded dictionaries.
"""
dict_cache = {}


def load_dict (path):
    """ Loads a dictionary from a file and returns it.
    Args:
        path (str): The path from which to load the dictionary.
    Returns:
        list of str: The requested dictionary.
    """
    if not path in dict_cache: # Load into cache if needed.
        dict = []
        with open(path, 'r') as target:
            for entry in target: # Load into memory.
                dict.append(entry.strip()) # Strip whitespace.
        dict_cache[path] = dict
    return dict_cache[path] # Get dictionary from cache.


def complies (val, length=0, lowers=0, uppers=0, digits=0, others=0, letters=0, classes=0, words=0, spec=[], invert=False):
    """ Checks whether or not a string complies with a password policy.
    Special additional requirements include:
        + `norep`: Disallow repeated characters.
        + `noconsec`: Disallow adjacent characters with consecutive codepoints.
        + `nodate`: Disallow 6-digit numeric strings that look like dates.
        + `dict:<file>`: Disallow passwords listed in a file (after converting to lowercase and removing non-letters).
    Args:
        val (str): The string to check.
        length (int): The minimum string length allowed.
        lowers (int): The minimum number of lowercase letters allowed.
        uppers (int): The minimum number of uppercase letters allowed.
        digits (int): The minimum number of digits allowed.
        others (int): The minimum number of symbols allowed.
        letters (int): The minimum number of letters allowed.
        classes (int): The minimum number of character classes allowed.
        words (int): The minimum number of words allowed.
        spec (list of str): Any special additional requirements.
        invert (bool): Whether to not to invert the policy.
    Returns:
        bool: True if the string is compliant, otherwise false.
    """
    complies_spec = True
    for req in spec:
        if req == 'norep':
            complies_spec = complies_spec and not contains_rep(val)
        elif req == 'noconsec':
            complies_spec = complies_spec and not contains_consec(val)
        elif req == 'nodate':
            complies_spec = complies_spec and not is_date(val)
        elif req.startswith('dict:'):
            complies_spec = complies_spec and not dict_normalise(val) in load_dict(req.split(':')[1])
    return invert ^ (len(val) >= length and
               count_lowers(val) >= lowers and
               count_uppers(val) >= uppers and
               count_digits(val) >= digits and
               count_symbols(val) >= others and
               count_classes(val) >= classes and
               count_letters(val) >= letters and
               count_words(val) >= words and
               complies_spec)
