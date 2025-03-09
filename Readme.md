# Vinted Shipping Calculator

## Overview

This program processes shipping transactions, applies discount rules, and generates the output.

1. **Read Data**: Load transactions from `input.txt`.

2. **Validation**:

   - Ensure data is formatted is correctly.
   - Validate the date is in ISO format (`YYYY-MM-DD`).
   - Check that package sizes and providers are valid.

3. **Processing**:

   - Ignore invalid transactions.
   - Apply discounts:
     - For large shipments from LP: The 3rd large shipment in a month is free.
     - For small shipments: Set the price to the lowest small package rate among providers.
     - Ensure that monthly discount limit is not exceeded.

4. **Output**:
   - Processed transactions are printed with relevant details: date, size, provider, price, and discount.

## Running Program

Execute `python main.py`

## Running Tests

Execute `python run_tests.py`
