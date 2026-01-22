"""Module for loading and validating bill data from CSV files."""

import pandas as pd


def load_validate_data(csv_path):
    """
    Read in a csv dataset through its path and validate its values

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
    valid_df = pd.read_csv(csv_path)
    required_cols = {"payer", "item_name", "item_price", "shared_by", "tax_pct", "tip_pct",}

    # Check for missing required columns
    missing = required_cols.difference(valid_df.columns)
    if missing:
        missing_str = ", ".join(sorted(missing))
        raise ValueError(f"Missing required column(s): {missing_str}")

    # Columns that must be numeric
    numeric_cols = ["item_price", "tax_pct", "tip_pct"]
    for col in numeric_cols:
        try:
            valid_df[col] = pd.to_numeric(valid_df[col])
        except Exception as exc:
            raise ValueError(f"Column '{col}' must be numeric.") from exc

    # Check item_price is non-negative
    for val in valid_df["item_price"]:
        if val < 0:
            raise ValueError("item_price values must be non-negative.")

    # Check tax_pct is between 0.05 and 0.15
    for val in valid_df["tax_pct"]:
        if val < 0.05 or val > 0.15:
            raise ValueError("tax_pct values must be between 0.05 and 0.15.")

    # Check tip_pct is between 0.0 and 0.50
    for val in valid_df["tip_pct"]:
        if val < 0.0 or val > 0.50:
            raise ValueError("tip_pct values must be between 0.0 and 0.50.")

    return valid_df
