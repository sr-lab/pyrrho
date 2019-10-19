import pandas as pd


def reselect (total, surplus, df):
    """ Models proportional reselection on a password probability distribution.

    Args:
        total (float): The total probability (should be approximately equal to 1).
        surplus (float): The surplus probability (should be less than or equal to `total`).
        df (DataFrame): The data frame containing the target field.
    """
    # Proportional reselection.
    divisor = total - surplus
    df['probability'] /= divisor#
    return df
