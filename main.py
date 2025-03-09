"""
Main entry point for the shipment processing application.

This module orchestrates the reading, processing, and output of shipment transactions.

Imports:
    - validators.read_transactions: Reads and validates transaction data from a file.
    - processor.process_transactions: Processes transactions by applying discount rules.
    - processor.write_output: Writes the processed transaction data to output.
"""

from validators import read_transactions
from processor import process_transactions, write_output


def main():
    """Main function to read, validate, process, and display transactions."""
    transactions = read_transactions("input.txt")
    processed_transactions = process_transactions(transactions)
    write_output(processed_transactions)


if __name__ == "__main__":
    main()
