"""
Discounts module for shipment transactions.

This module contains discount rules and logic for applying discounts
to shipment transactions. It manages discount limits, special rules,
and ensures correct pricing.

Imports:
    - collections.defaultdict: Handles monthly discount tracking.
    - models.Transaction, ProcessedTransaction: Represents shipment transactions.
"""

from collections import defaultdict
from models import Transaction, ProcessedTransaction

# Constants for shipment pricing
PRICES = {
    "LP": {"S": 1.50, "M": 4.90, "L": 6.90},
    "MR": {"S": 2.00, "M": 3.00, "L": 4.00},
}

MONTHLY_DISCOUNT_LIMIT = 10.0  # Monthly limit for discounts


class DiscountRule:
    """Base class for all discount rules."""

    def apply(self, transaction: Transaction, tracking_data: dict) -> tuple:
        """Apply a discount rule to a transaction.

        Args:
            transaction (Transaction): The transaction to evaluate.
            tracking_data (dict): Tracking information for discount limits.

        Returns:
            tuple: The new price and applied discount amount.
        """
        raise NotImplementedError


class SmallPackageDiscount(DiscountRule):
    """Discount rule for small-sized shipments."""

    def apply(self, transaction: Transaction, tracking_data: dict) -> tuple:
        """Apply the small package discount rule.

        If a small package shipment is not the lowest price, the price
        is adjusted to match the cheapest available.

        Args:
            transaction (Transaction): The transaction to evaluate.
            tracking_data (dict): Tracking information for discount limits.

        Returns:
            tuple: The new price and applied discount amount.
        """
        if transaction.size != "S":
            return PRICES[transaction.provider][transaction.size], 0.0

        lowest_price = min(PRICES["LP"]["S"], PRICES["MR"]["S"])
        current_price = PRICES[transaction.provider]["S"]

        if current_price > lowest_price:
            discount_amount = current_price - lowest_price
            return self.apply_monthly_limit(
                transaction, discount_amount, tracking_data
            )

        return current_price, 0.0

    @staticmethod
    def apply_monthly_limit(
        transaction: Transaction, discount_amount: float, tracking_data: dict
    ) -> tuple:
        """Apply the monthly discount limit.

        Ensures that discounts do not exceed the maximum allowed amount per month.

        Args:
            transaction (Transaction): The transaction being processed.
            discount_amount (float): The potential discount amount.
            tracking_data (dict): Tracking information for discount limits.

        Returns:
            tuple: The new price and final discount applied.
        """
        year_month = transaction.date[:7]
        used_discount = tracking_data[year_month]["discount"]

        if used_discount + discount_amount > MONTHLY_DISCOUNT_LIMIT:
            discount_amount = max(0, MONTHLY_DISCOUNT_LIMIT - used_discount)

        tracking_data[year_month]["discount"] += discount_amount
        new_price = PRICES[transaction.provider]["S"] - discount_amount

        return round(new_price, 2), round(discount_amount, 2)


class LargeLPThirdShipmentFree(DiscountRule):
    """Discount rule for the third 'L' shipment of LP each month."""

    def apply(self, transaction: Transaction, tracking_data: dict) -> tuple:
        """Apply the third 'L' package free rule for LP shipments.

        The third large 'LP' shipment each month gets a full discount.

        Args:
            transaction (Transaction): The transaction to evaluate.
            tracking_data (dict): Tracking information for discount limits.

        Returns:
            tuple: The new price and applied discount amount.
        """
        if transaction.size != "L" or transaction.provider != "LP":
            return PRICES[transaction.provider][transaction.size], 0.0

        year_month = transaction.date[:7]
        tracking_data[year_month]["L_LP_count"] += 1
        current_count = tracking_data[year_month]["L_LP_count"]

        if current_count == 3:
            discount_amount = PRICES["LP"]["L"]
            return self.apply_monthly_limit(
                transaction, discount_amount, tracking_data
            )

        return PRICES["LP"]["L"], 0.0

    @staticmethod
    def apply_monthly_limit(
        transaction: Transaction, discount_amount: float, tracking_data: dict
    ) -> tuple:
        """Apply the monthly discount limit."""
        year_month = transaction.date[:7]
        used_discount = tracking_data[year_month]["discount"]

        if used_discount + discount_amount > MONTHLY_DISCOUNT_LIMIT:
            discount_amount = max(0, MONTHLY_DISCOUNT_LIMIT - used_discount)

        tracking_data[year_month]["discount"] += discount_amount
        new_price = PRICES["LP"]["L"] - discount_amount

        return round(new_price, 2), round(discount_amount, 2)


class DiscountManager:
    """Manages and applies discount rules to transactions."""

    def __init__(self):
        """Initialize DiscountManager with discount rules and tracking data."""
        self.rules = [LargeLPThirdShipmentFree(), SmallPackageDiscount()]
        self.tracking_data = defaultdict(
            lambda: {"L_LP_count": 0, "discount": 0.0}
        )

    def apply_discounts(
        self, transaction: Transaction
    ) -> ProcessedTransaction:
        """Apply all applicable discount rules to a transaction.

        Determines the best available discount for a given transaction.

        Args:
            transaction (Transaction): The transaction to evaluate.

        Returns:
            ProcessedTransaction: The processed transaction with final price and discount.
        """
        best_price, best_discount = (
            PRICES[transaction.provider][transaction.size],
            0.0,
        )

        for rule in self.rules:
            price, discount = rule.apply(transaction, self.tracking_data)
            if price < best_price:
                best_price, best_discount = price, discount

        discount_display = best_discount if best_discount > 0 else "-"
        return ProcessedTransaction(
            transaction.date,
            transaction.size,
            transaction.provider,
            best_price,
            discount_display,
        )
