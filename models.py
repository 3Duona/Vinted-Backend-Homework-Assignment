"""
Defines data models for shipment transactions.

This module contains dataclasses representing different types of transactions.

Imports:
    - dataclasses.dataclass: Simplifies the creation of data classes.
    - typing.Union: Allows defining attributes that can have multiple types.
"""

from dataclasses import dataclass
from typing import Union


@dataclass
class Transaction:
    """Represents a valid shipment transaction."""

    date: str
    size: str
    provider: str


@dataclass
class ProcessedTransaction:
    """Represents a processed shipment transaction with price and discount details."""

    date: str
    size: str
    provider: str
    price: float
    discount: Union[float, str]  # "-" if no discount applied


@dataclass
class IgnoredTransaction:
    """Represents an invalid transaction."""

    data: str
