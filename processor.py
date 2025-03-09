"""
Processing module for handling transactions.

This module processes transactions, applies discounts, and writes output results.

Imports:
    - typing.List, Union: Defines type hints for function return values.
    - models.Transaction, models.ProcessedTransaction, models.IgnoredTransaction:
    Represents valid and ignored transactions.
    - discounts.DiscountManager: Class for the discount rules
"""

from typing import List, Union
from models import Transaction, ProcessedTransaction, IgnoredTransaction
from discounts import DiscountManager


def process_transactions(
    transactions: List[Union[Transaction, IgnoredTransaction]],
) -> List[Union[ProcessedTransaction, IgnoredTransaction]]:
    """Process a list of transactions using the DiscountManager.

    Each transaction is evaluated, and valid transactions receive applicable discounts.
    Ignored transactions remain unchanged.

    Args:
        transactions (List[Union[Transaction, IgnoredTransaction]]):
            A list of transactions to process.

    Returns:
        List[Union[ProcessedTransaction, IgnoredTransaction]]:
            A list of processed transactions, including discounted shipments and ignored entries.
    """
    discount_manager = DiscountManager()
    processed = []

    for transaction in transactions:
        if isinstance(transaction, IgnoredTransaction):
            processed.append(transaction)
        else:
            processed.append(discount_manager.apply_discounts(transaction))

    return processed


def write_output(
    transactions: List[Union[ProcessedTransaction, IgnoredTransaction]],
):
    """Write the processed transactions to the console.

    Each processed transaction is printed in a structured format.
    If a transaction is ignored, it is explicitly marked as "Ignored."

    Args:
        transactions (List[Union[ProcessedTransaction, IgnoredTransaction]]):
            A list of transactions to be displayed.
    """
    for transaction in transactions:
        if isinstance(transaction, IgnoredTransaction):
            print(f"{transaction.data} Ignored")
        else:
            discount_display = (
                f"{transaction.discount:.2f}"
                if isinstance(transaction.discount, float)
                else "-"
            )
            print(
                f"{transaction.date} {transaction.size} {transaction.provider} "
                f"{transaction.price:.2f} {discount_display}"
            )
