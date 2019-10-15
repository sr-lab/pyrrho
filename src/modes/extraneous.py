from math import floor
import pandas as pd

import string
import random


def gen_rand_pass (len):
    """ Generates a random password.

    Note that this password is not subject to a password composition policy.

    Args:
        len (int): The length of the password to generate.
    Returns:
        str: The generated password
    """
    alpha = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(alpha) for i in range(len))


def reselect (total, surplus, df):
    """ Models extraneous reselection on a password probability distribution.

    Args:
        total (float): The total probability (should be approximately equal to 1).
        surplus (float): The surplus probability (should be less than or equal to `total`).
        df (DataFrame): The data frame containing the target field.
    """
    # Extraneous reselection.
    single = df['probability'].min()
    extra_recs = floor(surplus / single)
    pwds = [gen_rand_pass(16) for i in range(0, extra_recs)]
    probabilities = [single for i in range(0, extra_recs)]
    df = df.append(pd.DataFrame({"password": pwds, "probability": probabilities}))
