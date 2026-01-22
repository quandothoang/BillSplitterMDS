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
    0   Ana          38.775
    1   Leo          26.075

    """
    # create `num_shared_people` and `individual_price` column inside `valid_df`
    valid_df['num_shared_people'] = 1 + valid_df['shared_by'].str.count(";")
    valid_df['individual_price'] = (valid_df['item_price']
                                    * (1 + valid_df['tax_pct'] + valid_df['tip_pct'])
                                    / valid_df['num_shared_people'])

    # get a list of the unique names of consumers
    # who appear in the `shared_by` column at least once
    all_consumers = set()
    for people in valid_df['shared_by']:
        all_consumers.update(people.split(';'))
    all_consumers = list(all_consumers)

    # initiate the dataframe `should_pay_df`
    should_pay_df = pd.DataFrame({
        'name': all_consumers,
        'should_pay': [0.0] * len(all_consumers)
    })

    # calculate the correct amount in the `should_pay` column
    for i, person in enumerate(all_consumers):
        amt_should_pay = valid_df[valid_df['shared_by'].str.contains(person)]['individual_price'].sum()
        should_pay_df.loc[i, 'should_pay'] = amt_should_pay

    return should_pay_df

