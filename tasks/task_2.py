"""
Task 2: Generator of real numbers from text and their summation.

Provides a generator that extracts floating-point numbers from a string
and a helper that sums them using any compatible callable.
"""

from decimal import ROUND_HALF_UP, Decimal
import re
from typing import Callable


def generator_numbers(text: str):
    """Yield every floating-point number found in *text* as a Decimal.

    Only standalone numbers are matched — values embedded inside words
    (e.g. ``abc1.23xyz``) are ignored thanks to word-boundary anchors.

    Args:
        text: Arbitrary string that may contain floating-point literals.

    Yields:
        Decimal: The next floating-point number found in *text*.
    """
    pattern = r"\b\d+\.\d+\b"
    for match in re.finditer(pattern, text):
        yield Decimal(match.group())


def sum_profit(text: str, func: Callable) -> Decimal:
    """Return the sum of all numbers produced by *func* applied to *text*.

    The result is rounded to two decimal places using ROUND_HALF_UP.

    Args:
        text: Input string passed to *func*.
        func: A callable that accepts a string and returns an iterable of
            Decimal values (e.g. :func:`generator_numbers`).

    Returns:
        Decimal: Total sum rounded to two decimal places.
    """
    total = Decimal("0.0")
    for amount in func(text):
        total += amount
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")
