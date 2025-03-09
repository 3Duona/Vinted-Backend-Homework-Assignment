"""
Unit tests for the transaction processing functions.

Tests:
    - test_process_valid_transaction: Ensures that valid transactions are processed correctly.
    - test_process_ignored_transaction: Ensures that ignored transactions remain unchanged.
    - test_process_multiple_transactions: Ensures that multiple transactions are processed correctly.
    - test_process_with_invalid_data: Ensures that mixed valid and ignored transactions are processed properly.
"""

import unittest
from processor import process_transactions
from models import Transaction, ProcessedTransaction, IgnoredTransaction


class TestProcessor(unittest.TestCase):
    def test_process_valid_transaction(self):
        transactions = [Transaction("2025-03-09", "S", "LP")]
        processed = process_transactions(transactions)
        self.assertEqual(len(processed), 1)
        self.assertIsInstance(processed[0], ProcessedTransaction)

    def test_process_ignored_transaction(self):
        transactions = [IgnoredTransaction("Invalid data")]
        processed = process_transactions(transactions)
        self.assertEqual(len(processed), 1)
        self.assertIsInstance(processed[0], IgnoredTransaction)

    def test_process_multiple_transactions(self):
        transactions = [
            Transaction("2025-03-09", "S", "MR"),
            Transaction("2025-03-10", "L", "LP"),
            Transaction("2025-03-11", "M", "MR"),
        ]
        processed = process_transactions(transactions)
        self.assertEqual(len(processed), 3)
        self.assertTrue(
            all(isinstance(t, ProcessedTransaction) for t in processed)
        )

    def test_process_with_invalid_data(self):
        transactions = [
            Transaction("2025-03-09", "S", "MR"),
            IgnoredTransaction("Invalid data"),
        ]
        processed = process_transactions(transactions)
        self.assertEqual(len(processed), 2)
        self.assertIsInstance(processed[0], ProcessedTransaction)
        self.assertIsInstance(processed[1], IgnoredTransaction)
