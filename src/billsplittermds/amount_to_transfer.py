"""Module for calculating money transfers to settle debts."""

from decimal import Decimal

import pandas as pd

CENT = Decimal("0.01")


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
    result_df : pandas.DataFrame
        A dataframe describing the required transfers with the following columns:

        - 'sender' : name of the person who should send money
        - 'receiver' : name of the person who should receive money
        - 'amount' : amount of money to be transferred

    Raises
    ------
    ValueError
        If required columns are missing from input dataframes.


    Examples
    --------
    >>> should_pay_df
        name   should_pay
    0   Leo     30.0
    1   Ana     30.0
    2   Mia     30.0

    >>> actually_paid_df
        name   actually_paid
    0   Leo     50.0
    1   Ana     40.0
    2   Mia     0.0

    >>> amount_to_transfer(should_pay_df, actually_paid_df)
        sender  receiver    amount
    0   Mia     Leo         20.0
    1   Mia     Ana         10.0
    """

    # Validate required columns in should_pay_df
    if 'name' not in should_pay_df.columns or 'should_pay' not in should_pay_df.columns:
        raise ValueError("should_pay_df must have columns 'name' and 'should_pay'")

    # Validate required columns in actually_paid_df
    if 'name' not in actually_paid_df.columns or 'actually_paid' not in actually_paid_df.columns:
        raise ValueError("actually_paid_df must have columns 'name' and 'actually_paid'")

    # Merge the two dataframes
    merged_df = pd.merge(should_pay_df, actually_paid_df, on='name', how='outer')

    # Fill NaN with 0 (in case someone only appears in one dataframe)
    merged_df['should_pay'] = merged_df['should_pay'].fillna(0)
    merged_df['actually_paid'] = merged_df['actually_paid'].fillna(0)

    # Calculate balance: positive means overpaid (should receive), negative means underpaid (should send)
    merged_df['balance'] = (
    merged_df['actually_paid'].apply(lambda x: Decimal(str(x))) -
    merged_df['should_pay'].apply(lambda x: Decimal(str(x))))

    # Separate into creditors (overpaid) and debtors (underpaid)
    balances = merged_df[['name', 'balance']].copy()

    # Create lists to track transfers
    transfers = []

    # Get creditors and debtors
    creditors = balances[balances['balance'] > CENT].copy()  # Small threshold for floating point
    debtors = balances[balances['balance'] < -CENT].copy()

    # Convert to dictionaries for easier manipulation
    creditor_dict = dict(zip(creditors['name'], creditors['balance']))
    debtor_dict = dict(zip(debtors['name'], -debtors['balance']))  # Make positive

    # Settle debts by matching debtors with creditors
    while creditor_dict and debtor_dict:
        # Get the largest creditor and debtor
        creditor = max(creditor_dict, key=creditor_dict.get)
        debtor = max(debtor_dict, key=debtor_dict.get)

        # Calculate transfer amount
        transfer_amount = min(creditor_dict[creditor], debtor_dict[debtor])

        if transfer_amount > CENT:  # Only record non-trivial transfers
            transfers.append({
                'sender': debtor,
                'receiver': creditor,
                'amount': transfer_amount.quantize(CENT)
            })

        # Update balances
        creditor_dict[creditor] -= transfer_amount
        debtor_dict[debtor] -= transfer_amount

        # Remove settled accounts
        if creditor_dict[creditor] < CENT:
            del creditor_dict[creditor]
        if debtor_dict[debtor] < CENT:
            del debtor_dict[debtor]

    # Create result dataframe
    if transfers:
        result_df = pd.DataFrame(transfers)
    else:
        result_df = pd.DataFrame(columns=['sender', 'receiver', 'amount'])

    return result_df

