"""Tests for individual_total_payments function."""

import pytest
import pandas as pd

from billsplittermds.individual_total_payments import individual_total_payments

class TestIndividualTotalPayments:
    """Test suite for individual_total_payments function."""
    
    @pytest.fixture
    def simple_df(self):
        """Create a simple dataframe with one item per payer."""
        return pd.DataFrame({
            'payer': ['Leo', 'Ana'],
            'item_name': ['candy', 'lunch'],
            'item_price': [10.0, 20.0],
            'shared_by': ['Leo', 'Ana'],
            'tax_pct': [0.0, 0.0],
            'tip_pct': [0.0, 0.0]
        })

    @pytest.fixture
    def multiple_items_df(self):
        """Create a dataframe where one person paid for multiple items."""
        return pd.DataFrame({
            'payer': ['Leo', 'Leo', 'Ana'],
            'item_name': ['candy', 'taxi', 'lunch'],
            'item_price': [10.0, 40.0, 20.0],
            'shared_by': ['Leo', 'Leo;Ana', 'Ana'],
            'tax_pct': [0.0, 0.0, 0.0],
            'tip_pct': [0.0, 0.0, 0.0]
        })
    
    @pytest.fixture
    def tax_tip_df(self):
        """Create a dataframe with tax and tip."""
        return pd.DataFrame({
            'payer': ['Leo', 'Ana'],
            'item_name': ['dinner', 'drinks'],
            'item_price': [100.0, 50.0],
            'shared_by': ['Leo;Ana', 'Leo;Ana'],
            'tax_pct': [0.10, 0.05],
            'tip_pct': [0.20, 0.15]
        })

    def test_input_type_validation(self):
        """Test that function raises TypeError for invalid input type."""
        with pytest.raises(TypeError):
            individual_total_payments("not a dataframe")

    def test_simple_single_items(self, simple_df):
        """Test calculation when each person paid for one item."""
        result = individual_total_payments(simple_df)
        
        assert isinstance(result, pd.DataFrame)
        assert set(result.columns) == {'name', 'actually_paid'}
        
        leo_paid = result[result['name'] == 'Leo']['actually_paid'].values[0]
        ana_paid = result[result['name'] == 'Ana']['actually_paid'].values[0]
        
        assert leo_paid == 10.0
        assert ana_paid == 20.0

    def test_multiple_items_same_payer(self, multiple_items_df):
        """Test that multiple items by same payer are summed."""
        result = individual_total_payments(multiple_items_df)
        
        # Leo paid for candy (10) and taxi (40) = 50
        # Ana paid for lunch (20) = 20
        leo_paid = result[result['name'] == 'Leo']['actually_paid'].values[0]
        ana_paid = result[result['name'] == 'Ana']['actually_paid'].values[0]
        
        assert leo_paid == 50.0
        assert ana_paid == 20.0

    def test_tax_and_tip_applied(self, tax_tip_df):
        """Test that tax and tip are correctly applied."""
        result = individual_total_payments(tax_tip_df)
        
        # [item_price] * (1 + [tax_pct] + [tip_pct])
        # Leo's dinner: 100 * (1 + 0.10 + 0.20) = 130
        # Ana's drinks: 50 * (1 + 0.05 + 0.15) = 60
        leo_paid = result[result['name'] == 'Leo']['actually_paid'].values[0]
        ana_paid = result[result['name'] == 'Ana']['actually_paid'].values[0]
        
        assert abs(leo_paid - 130.0) < 0.01
        assert abs(ana_paid - 60.0) < 0.01

    def test_returns_correct_column_names(self, simple_df):
        """Test that output has correct column names."""
        result = individual_total_payments(simple_df)
        assert list(result.columns) == ['name', 'actually_paid']

    def test_total_paid_equals_sum_of_item_costs(self):
        """Test that sum of actually_paid equals total cost of all items."""
        df = pd.DataFrame({
            'payer': ['Leo', 'Ana', 'Mia'],
            'item_name': ['a', 'b', 'c'],
            'item_price': [100.0, 50.0, 75.0],
            'shared_by': ['Leo', 'Ana', 'Mia'],
            'tax_pct': [0.10, 0.05, 0.08],
            'tip_pct': [0.20, 0.15, 0.18]
        })
        
        result = individual_total_payments(df)
        
        # Calculate expected total
        total_cost = (100 * (1 + 0.10 + 0.20)) + (50 * (1 + 0.05 + 0.15)) + (75 * (1 + 0.08 + 0.18))
        total_paid = result['actually_paid'].sum()
        
        assert abs(total_paid - total_cost) < 0.01
