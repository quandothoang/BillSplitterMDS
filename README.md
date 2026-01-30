# BillSplitterMDS


[![build](https://github.com/UBC-MDS/BillSplitterMDS/actions/workflows/build.yml/badge.svg)](https://github.com/UBC-MDS/BillSplitterMDS/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/UBC-MDS/BillSplitterMDS/branch/main/graph/badge.svg)](https://codecov.io/gh/UBC-MDS/BillSplitterMDS)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://ubc-mds.github.io/BillSplitterMDS/)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package to help groups split trip bills fairly among participants.

## Summary

When a group of people travel together, different people often pay for different expenses throughout the trip. At the end, it can be complicated to figure out how much each person actually owes and how money should be transferred to settle all debts fairly. **BillSplitterMDS** simplifies this process by reading expense data from a CSV file and calculating the optimal transfers needed to balance everyone's contributions.

## Create the project environment

Please run the following command in bash terminal:

```bash
conda env create -f environment.yml
```

After the environment is created, activate it through the following:

```bash
conda activate billsplittermds
```

## Installation

Please change the directory to the root directory and run:

```bash
pip install -i https://test.pypi.org/simple/ billsplittermds
```

If the above does not work, use the following (recommended):

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ billsplittermds
```


## Running the function tests

To verify that each of the functions work appropriately, function tests are written in python scripts. To run these tests go to the root project directory in the terminal and write the following command:

```
pytest tests/
```

## Build documentation

Please go to the root directory first and run:

```bash
quartodoc build
```

Following that, run another command:

```bash
quarto preview
```

Then there will be a window popped up in your browser showing the rendered documentation webpage.

## Deploy documentation

GitHub pages have been set up to automate deployment. Please go to this URL to see the rendered homepage of our project:

https://ubc-mds.github.io/BillSplitterMDS/

To see the documentation page of our 4 functions, please visit the following, or click the `Reference` tab at the top of the homepage:

https://ubc-mds.github.io/BillSplitterMDS/reference/

## Functions

The package provides four main functions:

- **`load_validate_data(csv_path)`**: Reads a CSV file containing trip expense data and validates that tax and tip percentages are within reasonable ranges. Returns a validated pandas DataFrame.

- **`split_by_item(valid_df)`**: Calculates how much each person should pay based on the items they shared. Computes individual costs by dividing item prices (with tax and tip) among sharers, then aggregates totals per person.

- **`individual_total_payments(valid_df)`**: Calculates the total amount each person actually paid during the trip by summing up all bills paid by each person.

- **`amount_to_transfer(should_pay_df, actually_paid_df)`**: Determines the money transfers needed to settle all debts. Takes the outputs of `split_by_item()` and `individual_total_payments()` to compute who owes money to whom.

## Input CSV Format

The CSV file should have the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `payer` | Name of person who paid | Amy |
| `item_name` | Description of expense | Pasta |
| `item_price` | Price before tax/tip | 18 |
| `shared_by` | Names separated by semicolons | Amy;Ben |
| `tax_pct` | Tax as decimal | 0.05 |
| `tip_pct` | Tip as decimal | 0.12 |

Example CSV:
```
payer,item_name,item_price,shared_by,tax_pct,tip_pct
Amy,Pasta,18,Amy,0.05,0.12
Sam,Taxi,33,Amy;Ben;Sam;Joe,0.05,0.00
Ben,double-room,230,Amy;Ben,0.12,0.04
```

## Usage

```python
from billsplittermds import (
    load_validate_data,
    split_by_item,
    individual_total_payments,
    amount_to_transfer
)

# Load and validate the expense data
df = load_validate_data("trip_expenses.csv")

# Calculate what each person should pay
should_pay = split_by_item(df)

# Calculate what each person actually paid
actually_paid = individual_total_payments(df)

# Get the transfers needed to settle up
transfers = amount_to_transfer(should_pay, actually_paid)
print(transfers)
```

## Python Ecosystem

There are several expense-splitting apps and packages available:

- [Splitwise](https://www.splitwise.com/) - A popular mobile/web app for splitting bills (not a Python package)
- [split-bill](https://pypi.org/project/split-bill/) - A simple Python package for equal bill splitting

**BillSplitterMDS** differs from these by focusing specifically on trip expenses where items can be shared by different subsets of people, with configurable tax and tip percentages per item.

## Contributors

- Quan Hoang
- Jessie Liang
- Norton Yu
- Omar Ramos

## License

MIT License

<!-- Dev workflow proof commit -->
