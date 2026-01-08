"""Module for calculating money transfers to settle debts."""

import pandas as pd


def amount_to_transfer(should_pay_df, actually_paid_df):
    """
    Compute money transfers required to settle individual balances.

    This function takes the outputs of 'split_by_item' and 'individual_total_payments' functions and determines how much money should be transferred between individuals, so that each person's final spending equals the amount they should have paid.

    Parameters
    ----------
    should_pay_df : pandas.DataFrame
        Dataframe containing the amount each individual should pay according to splitting.
        Typically the output of 'split_by_item'.

    actually_paid_df : pandas.DataFrame
        Dataframe containing the amount each individual actually paid.
        Typically the output of 'individual_total_payments'.

    Returns
    -------
    pandas.DataFrame
        A dataframe describing the required transfers with the following columns:

        - 'sender' : name of the person who should send money
        - 'receiver' : name of the person who should receive money
        - 'amount' : amount of money to be transferred

    Examples
    --------
    >>> should_pay_df
        name   individual_price
    0   Leo     45.50
    1   Ana     19.35
    2   Mia     30.00

    >>> actually_paid_df
        payer   actual_payment
    0   Leo     39.45
    1   Ana     25.40
    2   Mia     10.00

    >>> amount_to_transfer(should_pay_df, actually_paid_df)
        sender  receiver    amount
    0   Leo     Ana         6.05
    1   Mia     Leo         20.00
    """
    pass
