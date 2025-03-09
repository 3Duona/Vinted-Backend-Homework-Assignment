"""
Unit tests for the transaction validation functions.

Tests:
    - test_valid_transaction: Ensures that a valid transaction string is parsed correctly.
    - test_invalid_transaction: Ensures that an invalid transaction string returns an `IgnoredTransaction`.
"""

import unittest
from validators import validate_transaction
from models import Transaction, IgnoredTransaction


class TestValidators(unittest.TestCase):
    def test_valid_transaction(self):
        valid_line = "2025-03-09 S LP"
        transaction = validate_transaction(valid_line)
        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(transaction.date, "2025-03-09")
        self.assertEqual(transaction.size, "S")
        self.assertEqual(transaction.provider, "LP")

    def test_invalid_transaction(self):
        invalid_line = "2025-03-09 XL LP"
        transaction = validate_transaction(invalid_line)
        self.assertIsInstance(transaction, IgnoredTransaction)
