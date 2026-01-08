"""Module for calculating how much each person should pay."""

import pandas as pd


def split_by_item(valid_df):
    """
    Calculates a derived column called individual_price, which is the amount 
    of this item that an individual should pay after splitting the bill evenly among 
    all people who consumed this item. Then we sum each person’s individual_price
    to get the total amount that this individual should pay. In brief, this function calculates
    how much each individual needs to pay in total during the trip after splitting the bill
    by item.

    Parameters
    ----------
    valid_df : pandas.DataFrame
        A dataframe after being validated with columns 'payer', 
        'item_name', 'item_price', 'shared_by', 'tax_pct', and 'tip_pct'.

    Returns
    -------
    should_pay_df : pandas.DataFrame
        Dataframe with columns 'individual' and 'should_pay'.

    Examples
    --------
    >>> valid_df
        payer   item_name  item_price  shared_by  tax_pct  tip_pct
    0   Leo     candy      10.0        Leo        0.12     0.15
    1   Leo     taxi       25.0        Leo;Ana    0.07     0.0
    2   Ana     lunch      20.0        Ana        0.12     0.15

    >>> split_by_item(valid_df)
        name         should_pay
    0   Leo          26.255
    1   Ana          39.135
    
    """
    pass
