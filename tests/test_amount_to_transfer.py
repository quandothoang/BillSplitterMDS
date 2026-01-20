"""Tests for amount_to_transfer function."""

import pytest
import pandas as pd

from billsplittermds.amount_to_transfer import amount_to_transfer


class TestAmountToTransfer:
    """Test suite for amount_to_transfer function."""

    @pytest.fixture
    def simple_transfer_dfs(self):
        """Create dataframes where one person owes another."""
        should_pay = pd.DataFrame({
            'name': ['Leo', 'Ana'],
            'should_pay': [50.0, 50.0]
        })
        actually_paid = pd.DataFrame({
            'name': ['Leo', 'Ana'],
            'actually_paid': [100.0, 0.0]
        })
        return should_pay, actually_paid
    
    def test_no_transfers_when_balanced(self):
        """Test that no transfers are needed when everyone paid their share."""
        should_pay = pd.DataFrame({
            'name': ['Leo', 'Ana', 'Mia'],
            'should_pay': [30.0, 30.0, 30.0]
        })
        actually_paid = pd.DataFrame({
            'name': ['Leo', 'Ana', 'Mia'],
            'actually_paid': [30.0, 30.0, 30.0]
        })

        result = amount_to_transfer(should_pay, actually_paid)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_simple_transfer(self, simple_transfer_dfs):
        """Test simple case where one person owes another."""
        
        should_pay, actually_paid = simple_transfer_dfs
        result = amount_to_transfer(should_pay, actually_paid)

        assert len(result) == 1
        assert result.iloc[0]['sender'] == 'Ana'
        assert result.iloc[0]['receiver'] == 'Leo'
        assert result.iloc[0]['amount'] == 50.0

    def test_multiple_transfers(self):
        """Test case with multiple transfers needed."""
        should_pay = pd.DataFrame({
            'name': ['Leo', 'Ana', 'Mia'],
            'should_pay': [30.0, 30.0, 30.0]
        })
        actually_paid = pd.DataFrame({
            'name': ['Leo', 'Ana', 'Mia'],
            'actually_paid': [50.0, 40.0, 0.0]
        })

        result = amount_to_transfer(should_pay, actually_paid)

        assert len(result) == 2
        total_from_mia = result[result['sender'] == 'Mia']['amount'].sum()
        assert total_from_mia == 30.0

    def test_missing_column_should_pay_raises_value_error(self):
        """Test that missing column in should_pay_df raises ValueError."""
        should_pay = pd.DataFrame({'name': ['Leo'], 'wrong_column': [30.0]})
        actually_paid = pd.DataFrame({'name': ['Leo'], 'actually_paid': [30.0]})

        with pytest.raises(ValueError) as exc_info:
            amount_to_transfer(should_pay, actually_paid)
        assert "should_pay_df must have columns" in str(exc_info.value)
        assert exc_info.type == ValueError

    def test_missing_column_actually_paid_raises_value_error(self):
        """Test that missing column in actually_paid_df raises ValueError."""
        should_pay = pd.DataFrame({'name': ['Leo'], 'should_pay': [30.0]})
        actually_paid = pd.DataFrame({'name': ['Leo'], 'wrong_column': [30.0]})

        with pytest.raises(ValueError) as exc_info:
            amount_to_transfer(should_pay, actually_paid)
        assert "actually_paid_df must have columns" in str(exc_info.value)
        assert exc_info.type == ValueError

    def test_output_columns(self, simple_transfer_dfs):
        """Test that output has correct column names."""
        should_pay, actually_paid = simple_transfer_dfs
        result = amount_to_transfer(should_pay, actually_paid)
        
        assert set(result.columns) == {'sender', 'receiver', 'amount'}
