"""
Integration tests for full transaction processing.

Tests:
    - test_full_transaction_processing: Ensures that a list of transactions is correctly processed, including validation, discount application, and output generation.
"""

import unittest
from models import Transaction, IgnoredTransaction
from processor import process_transactions


class TestIntegration(unittest.TestCase):
    def test_full_transaction_processing(self):
        transactions = [
            Transaction("2015-02-01", "S", "MR"),
            Transaction("2015-02-02", "S", "MR"),
            Transaction("2015-02-03", "L", "LP"),
            Transaction("2015-02-05", "S", "LP"),
            Transaction("2015-02-06", "S", "MR"),
            Transaction("2015-02-06", "L", "LP"),
            Transaction("2015-02-07", "L", "MR"),
            Transaction("2015-02-08", "M", "MR"),
            Transaction("2015-02-09", "L", "LP"),
            Transaction("2015-02-10", "L", "LP"),
            Transaction("2015-02-10", "S", "MR"),
            Transaction("2015-02-10", "S", "MR"),
            Transaction("2015-02-11", "L", "LP"),
            Transaction("2015-02-12", "M", "MR"),
            Transaction("2015-02-13", "M", "LP"),
            Transaction("2015-02-15", "S", "MR"),
            Transaction("2015-02-17", "L", "LP"),
            Transaction("2015-02-17", "S", "MR"),
            Transaction("2015-02-24", "L", "LP"),
            IgnoredTransaction("2015-02-29 CUSPS"),
            Transaction("2015-03-01", "S", "MR"),
        ]

        processed = process_transactions(transactions)

        expected_output = [
            "2015-02-01 S MR 1.50 0.50",
            "2015-02-02 S MR 1.50 0.50",
            "2015-02-03 L LP 6.90 -",
            "2015-02-05 S LP 1.50 -",
            "2015-02-06 S MR 1.50 0.50",
            "2015-02-06 L LP 6.90 -",
            "2015-02-07 L MR 4.00 -",
            "2015-02-08 M MR 3.00 -",
            "2015-02-09 L LP 0.00 6.90",
            "2015-02-10 L LP 6.90 -",
            "2015-02-10 S MR 1.50 0.50",
            "2015-02-10 S MR 1.50 0.50",
            "2015-02-11 L LP 6.90 -",
            "2015-02-12 M MR 3.00 -",
            "2015-02-13 M LP 4.90 -",
            "2015-02-15 S MR 1.50 0.50",
            "2015-02-17 L LP 6.90 -",
            "2015-02-17 S MR 1.90 0.10",
            "2015-02-24 L LP 6.90 -",
            "2015-02-29 CUSPS Ignored",
            "2015-03-01 S MR 1.50 0.50",
        ]

        # Capture the output from the processed transactions
        output_lines = []
        for transaction in processed:
            if isinstance(transaction, IgnoredTransaction):
                output_lines.append(f"{transaction.data} Ignored")
            else:
                discount_display = (
                    f"{transaction.discount:.2f}"
                    if isinstance(transaction.discount, float)
                    else "-"
                )
                output_lines.append(
                    f"{transaction.date} {transaction.size} {transaction.provider} "
                    f"{transaction.price:.2f} {discount_display}"
                )

        # Compare the processed output with the expected output
        self.assertEqual(output_lines, expected_output)


if __name__ == "__main__":
    unittest.main()
