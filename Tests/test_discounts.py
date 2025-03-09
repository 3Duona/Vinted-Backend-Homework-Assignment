"""
Unit tests for the discount application logic.

Tests:
    - test_small_package_discount: Ensures the small package discount is applied correctly.
    - test_large_lp_third_shipment_free: Ensures the large LP third shipment free discount is applied correctly.
    - test_large_lp_third_shipment_discount: Ensures that the third shipment free discount is correctly applied after the second large LP shipment.
"""

import unittest
from discounts import DiscountManager
from discounts import SmallPackageDiscount, LargeLPThirdShipmentFree
from models import Transaction
from collections import defaultdict


class TestDiscounts(unittest.TestCase):
    def setUp(self):
        self.discount_manager = DiscountManager()
        self.tracking_data = defaultdict(
            lambda: {"L_LP_count": 0, "discount": 0.0}
        )

    def test_small_package_discount(self):
        transaction = Transaction("2025-03-09", "S", "LP")
        discount_rule = SmallPackageDiscount()
        price, discount = discount_rule.apply(transaction, self.tracking_data)
        self.assertEqual(price, 1.50)
        self.assertEqual(discount, 0.0)

    def test_large_lp_third_shipment_free(self):
        transaction = Transaction("2025-03-09", "L", "LP")
        discount_rule = LargeLPThirdShipmentFree()
        price, discount = discount_rule.apply(transaction, self.tracking_data)
        self.assertEqual(price, 6.90)
        self.assertEqual(discount, 0.0)

    def test_large_lp_third_shipment_discount(self):
        self.tracking_data["2025-03"]["L_LP_count"] = 2  # Third Shipment
        transaction = Transaction("2025-03-09", "L", "LP")
        discount_rule = LargeLPThirdShipmentFree()
        price, discount = discount_rule.apply(transaction, self.tracking_data)
        self.assertEqual(price, 0.00)
        self.assertEqual(discount, 6.90)
