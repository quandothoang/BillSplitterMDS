"""Module for loading and validating bill data from CSV files."""

import pandas as pd


def load_validate_data(csv_path):
    """
    Reads the raw csv file and validates numeric columns. Specifically, 
    item price should be positive, tip percentage should be non-negative,
    and tax percentage should be positive. Prints an error if the
    validation process fails.

    Parameters
    ----------
    csv_path : str
        The string of path from which we read the raw data.

    Returns
    -------
    validated_df : pandas.DataFrame
        Dataframe that is read and validated from the given path.

    Examples
    --------
    >>> load_validate_data("../../data/raw.csv")
        payer   item_name        item_price  shared_by     tax_pct  tip_pct
    0   Amy      pasta           10.0        Amy           0.12     0.15
    1   Sam      taxi            25.0        Amy;Sam;Ben   0.07     0.0
    2   Ben      double-room     20.0        Amy;Ben       0.12     0.15
    
    """
    pass
