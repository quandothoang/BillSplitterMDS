"""Module for calculating how much each person actually paid."""

import pandas as pd


def individual_total_payments(valid_df):
    """
    Calculate the net amount to pay per item and return a dataframe with the total payment amount per person.

    First, this function takes in valid payments dataframe and derives a new column 'item_paymant' which is the total cost of each item including tax and tip. 
    Then, it groups the datafram by the person who originally paid for the item and sums up the cost.

    Parameters
    ----------
    valid_df : pandas.DataFrame
        A dataframe containing validated data read from the input CSV file.
        Typically the output of load_validate_data() function.

    Returns
    -------
    actually_paid_df : pandas.DataFrame
        Dataframe with columns 'payer' and 'actually_paid'.

    Examples
    --------
    >>> valid_df

        payer   item_name  item_price  shared_by  tax_pct  tip_pct
    0   Leo     candy      10.0        Leo        0.12     0.15
    1   Leo     taxi       25.0        Leo;Ana    0.07     0.0
    2   Ana     lunch      20.0        Ana        0.12     0.15
    
    >>> individual_total_payments(valid_df)
        name   actually_paid
    0   Leo     39.45
    1   Ana     25.40

    """
    # Validate input parameter is of type pandas.DataFrame
    if isinstance(valid_df, pd.DataFrame) is False:
        raise TypeError(f"Input parameter 'valid_df' must be of type pandas.DataFrame, got {type(valid_df)} instead.")

    # Calculate item_payment including tax and tip
    valid_df['item_payment'] = valid_df['item_price'] * (1 + valid_df['tax_pct'] + valid_df['tip_pct'])

    # Group by payer and sum the item_payment to get actually_paid output
    actually_paid_df = valid_df.groupby('payer', as_index=False)['item_payment'].sum()
    actually_paid_df.rename(columns={'payer': 'name', 'item_payment': 'actually_paid'}, inplace=True)

    return actually_paid_df
