"""Module for calculating how much each person actually paid."""

import pandas as pd


def individual_total_payments(valid_df):
    """
    Calculate the net amount to pay per item and return a dataframe with the total payment amount per person.

    First, this function takes in valid payments dataframe and derives a new column 'item_paymant' which is the total cost of each item including tax and tip. Then, it groups the datafram by the person who originally paid for the item and sums up the cost.

    Parameters
    ----------
    valid_df : pandas.DataFrame
        A dataframe containing valid payments with columns 'payer', 'item_price', 'tax_pct', and 'tip_pct'.

    Returns
    -------
    actually_paid_df : pandas.DataFrame
        Dataframe with columns 'payer' and 'actual_payment'.

    Examples
    --------
    >>> valid_df
        payer   item_price  tax_pct  tip_pct
    0   Leo     10.0        0.12     0.15
    1   Leo     25.0        0.07     0.0
    2   Ana     20.0        0.12     0.15

    >>> individual_total_payments(valid_df)
        payer   actual_payment
    0   Leo     39.45
    1   Ana     25.40

    """
    pass
