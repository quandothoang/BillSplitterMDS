"""Module for loading and validating bill data from CSV files."""

import pandas as pd


def load_validate_data(csv_path):
    """

    Parameters
    ----------
    csv_path : str
        The string of path from which we read the raw data.

    Returns
    -------
    valid_df : pandas.DataFrame
        Dataframe that is read and validated from the given path.

    Examples
    --------
    >>> load_validate_data("../../data/raw.csv")
        payer   item_name        item_price  shared_by     tax_pct  tip_pct
    0   Amy      pasta           10.0        Amy           0.12     0.15
    1   Sam      taxi            25.0        Amy;Sam;Ben   0.07     0.0
    2   Ben      double-room     20.0        Amy;Ben       0.12     0.15
    
    """
    raise NotImplementedError("load_validate_data not implemented yet")
