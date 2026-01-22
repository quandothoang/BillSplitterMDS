import pandas as pd
import pytest

from billsplittermds.load_validate_data import load_validate_data


def test_load_validate_data_basic(tmp_path):
    """
    Basic test: valid CSV should return a 1-row DataFrame
    with the expected columns.
    """
    # create a tiny CSV file in a temp folder (like having tests/text.txt)
    csv_content = (
        "payer,item_name,item_price,shared_by,tax_pct,tip_pct\n"
        "Amy,Pasta,18,Amy,0.05,0.12\n"
    )
    csv_path = tmp_path / "trip.csv"
    csv_path.write_text(csv_content)

    df = load_validate_data(csv_path)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 6)

def test_load_validate_data_missing_column(tmp_path):
    """
    If a required column is missing, raise ValueError.
    """
    # tip_pct column is missing here
    csv_content = (
        "payer,item_name,item_price,shared_by,tax_pct\n"
        "Amy,Pasta,18,Amy,0.05\n"
    )
    csv_path = tmp_path / "trip_missing_col.csv"
    csv_path.write_text(csv_content)

    with pytest.raises(ValueError):
        load_validate_data(csv_path)

def test_load_validate_data_tax_out_of_range(tmp_path):
    """
    If tax_pct is outside [0.05, 0.15] or tip_pct is outside [0, 0.50], raise ValueError.
    """
    # tax is too low (0.02 < 0.05)
    csv_content = (
        "payer,item_name,item_price,shared_by,tax_pct,tip_pct\n"
        "Amy,Pasta,18,Amy,0.02,0.10\n"
    )
    csv_path = tmp_path / "trip_bad_tax.csv"
    csv_path.write_text(csv_content)

    with pytest.raises(ValueError):
        load_validate_data(csv_path)


def test_load_validate_data_non_numeric_tax(tmp_path):
    """
    If tax_pct or tip_pct is not numeric, raise ValueError.
    """
    csv_content = (
        "payer,item_name,item_price,shared_by,tax_pct,tip_pct\n"
        "Amy,Pasta,18,Amy,hello,0.12\n"
    )
    csv_path = tmp_path / "trip_non_numeric.csv"
    csv_path.write_text(csv_content)

    with pytest.raises(ValueError):
        load_validate_data(csv_path)


def test_load_validate_data_negative_price(tmp_path):
    """
    If item_price is negative, raise ValueError.
    """
    csv_content = (
        "payer,item_name,item_price,shared_by,tax_pct,tip_pct\n"
        "Amy,Pasta,-18,Amy,0.05,0.12\n"
    )
    csv_path = tmp_path / "trip_negative.csv"
    csv_path.write_text(csv_content)

    with pytest.raises(ValueError):
        load_validate_data(csv_path)

def test_load_validate_data_nonexistent_path():
    """
    Loading a non-existent file path should raise an exception.
    """
    with pytest.raises(Exception):
        load_validate_data("this/does/not/exist.csv")
