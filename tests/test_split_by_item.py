"""Tests for the function split_by_item()."""

import pandas as pd
import pytest

from billsplittermds.split_by_item import split_by_item


class TestSplitByItem:
    """Test functions for the function split_by_item()"""


    # Below are 4 sample dataframes used as inputs:
    @pytest.fixture
    def simple_df(self):
        """
        A simple dataframe where each item
        was consumed by just one person.
        """
        return pd.DataFrame({
            'payer': ['Leo', 'Ana'],
            'item_name': ['candy', 'lunch'],
            'item_price': [10.0, 20.0],
            'shared_by': ['Leo', 'Ana'],
            'tax_pct': [0.0, 0.0],
            'tip_pct': [0.0, 0.0]
        })

    @pytest.fixture
    def shared_item_df(self):
        """
        A dataframe where some items were
        shared by more than one person.
        """
        return pd.DataFrame({
            'payer': ['Leo', 'Leo'],
            'item_name': ['taxi', 'dinner'],
            'item_price': [40.0, 100.0],
            'shared_by': ['Leo;Ana', 'Leo;Ana;Mia;Joe'],
            'tax_pct': [0.0, 0.0],
            'tip_pct': [0.0, 0.0]
        })

    @pytest.fixture
    def tax_tip_df(self):
        """A dataframe with non-zero tax and tip percentage."""
        return pd.DataFrame({
            'payer': ['Leo'],
            'item_name': ['dinner'],
            'item_price': [100.0],
            'shared_by': ['Leo;Ana'],
            'tax_pct': [0.10],
            'tip_pct': [0.20]
        })

    @pytest.fixture
    def comprehensive_df(self):
        """
        A dataframe with non-zero tax and tip percentage,
        and some items were split by more than one people.
        """
        return pd.DataFrame({
            'payer': ['Leo', 'Ana'],
            'item_name': ['taxi', 'lunch'],
            'item_price': [50.0, 30.0],
            'shared_by': ['Leo;Ana;Mia', 'Ana'],
            'tax_pct': [0.10, 0.05],
            'tip_pct': [0.15, 0.10]
        })



    # Below are the 5 test functions:
    def test_simple_no_sharing(self, simple_df):
        """When all items are not shared."""
        result = split_by_item(simple_df)
        assert isinstance(result, pd.DataFrame)
        assert set(result.columns) == {'name', 'should_pay'}

        leo_pay = result[result['name'] == 'Leo']['should_pay'].values[0]
        ana_pay = result[result['name'] == 'Ana']['should_pay'].values[0]

        assert leo_pay == 10.0
        assert ana_pay == 20.0

    def test_shared_items_split_evenly(self, shared_item_df):
        """When some items were actually shared."""
        result = split_by_item(shared_item_df)

        leo_pay = result[result['name'] == 'Leo']['should_pay'].values[0]
        ana_pay = result[result['name'] == 'Ana']['should_pay'].values[0]
        mia_pay = result[result['name'] == 'Mia']['should_pay'].values[0]
        joe_pay = result[result['name'] == 'Joe']['should_pay'].values[0]

        assert leo_pay == 45.0
        assert ana_pay == 45.0
        assert mia_pay == 25.0
        assert joe_pay == 25.0

    def test_nonzero_tax_and_tip(self, tax_tip_df):
        """When tax and tip percentages are non-zero."""
        result = split_by_item(tax_tip_df)

        leo_pay = result[result['name'] == 'Leo']['should_pay'].values[0]
        ana_pay = result[result['name'] == 'Ana']['should_pay'].values[0]

        assert leo_pay == 65
        assert ana_pay == 65

    def test_returns_all_sharers(self, shared_item_df):
        """
        All consumers contained in the `shared_by` column
        should appear in the `name` column of the result.
        """
        result = split_by_item(shared_item_df)
        names = set(result['name'])
        assert names == {'Leo', 'Ana', 'Mia', 'Joe'}

    def test_total_should_pay_equals_total_cost(self, comprehensive_df):
        """
        Sum of the `should_pay` column of the result dataframe
        should equal to the total cost of all items.
        """
        result = split_by_item(comprehensive_df)

        # Calculate expected total
        total_cost = (50.0 * (1 + 0.10 + 0.15) + 30.0 * (1 + 0.05 + 0.10))
        total_should_pay = result['should_pay'].sum()
        assert abs(total_should_pay - total_cost) < 0.001

    def test_invalid_input_type(self):
        """
        Non-DataFrame input should raise an exception.
        """
        with pytest.raises(Exception):
            split_by_item("not a dataframe")

