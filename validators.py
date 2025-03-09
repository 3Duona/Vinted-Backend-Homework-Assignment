"""
Handles input validation for shipment transactions.

This module provides functions for reading and validating transaction data.

Imports:
    - os: Used to check for file existence and validate file extension.
    - datetime.datetime: Used to validate the date format in transactions.
    - typing.List, Union: Defines type hints for function return values.
    - models.Transaction, models.IgnoredTransaction: Represents valid and ignored transactions.
"""

import os
import datetime
from typing import List, Union
from models import Transaction, IgnoredTransaction


def read_transactions(
    file_name,
) -> List[Union[Transaction, IgnoredTransaction]]:
    """Read transactions from a file and return a list of validated Transaction
    or IgnoredTransaction objects.

    Args:
        file_name (str): The name of the file containing transactions.

    Returns:
        List[Union[Transaction, IgnoredTransaction]]: A list of validated transactions.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a .txt file or is empty.
    """
    if not os.path.isfile(file_name):
        raise FileNotFoundError(
            f"Error: The file '{file_name}' does not exist."
        )

    if not file_name.lower().endswith(".txt"):
        raise ValueError(
            f"Error: Invalid file type. Expected a .txt file, got '{file_name}'."
        )

    transactions = []

    with open(file_name, encoding="utf-8") as file:
        lines = file.readlines()

        if not lines:
            raise ValueError(f"Error: The file '{file_name}' is empty.")

        for line in lines:
            transaction = validate_transaction(line.strip())
            transactions.append(transaction)

    return transactions


def validate_transaction(line: str) -> Union[Transaction, IgnoredTransaction]:
    """Validate and convert a raw transaction line into a Transaction object.

    Args:
        line (str): A single line from the input file.

    Returns:
        Union[Transaction, IgnoredTransaction]: A valid Transaction object or an IgnoredTransaction.
    """
    parts = line.split()
    if len(parts) != 3:
        return IgnoredTransaction(line)

    date, size, provider = parts

    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return IgnoredTransaction(line)

    if size not in {"S", "M", "L"} or provider not in {"LP", "MR"}:
        return IgnoredTransaction(line)

    return Transaction(date, size, provider)
