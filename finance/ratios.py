"""Percentage and Ratio calculation tools."""

from decimal import Decimal, ROUND_HALF_UP
import math
from typing import Dict, Tuple, Union


def _to_decimal(val: Union[int, float, str, Decimal]) -> Decimal:
    if isinstance(val, Decimal):
        return val
    cleaned = str(val).replace(",", "").replace("%", "").strip()
    return Decimal(cleaned) if cleaned else Decimal("0")


def _round_clean(val: Decimal, places: int = 4) -> Decimal:
    factor = Decimal("10") ** -places
    return val.quantize(factor, rounding=ROUND_HALF_UP).normalize()


def percentage_of(
    percent: Union[int, float, str, Decimal],
    total_value: Union[int, float, str, Decimal],
) -> Decimal:
    """Calculate X% of Y. E.g., 20% of 500 = 100."""
    p = _to_decimal(percent)
    t = _to_decimal(total_value)
    return _round_clean((p / Decimal("100")) * t, places=2)


def percentage_change(
    old_value: Union[int, float, str, Decimal],
    new_value: Union[int, float, str, Decimal],
) -> Dict[str, Union[Decimal, str]]:
    """Calculate percentage increase or decrease from old to new value.
    
    Formula: ((New - Old) / Old) * 100
    """
    old = _to_decimal(old_value)
    new = _to_decimal(new_value)

    if old == 0:
        raise ValueError("Initial value cannot be zero when calculating percentage change")

    diff = new - old
    pct = _round_clean((diff / abs(old)) * Decimal("100"), places=2)

    if diff > 0:
        change_type = "increase"
    elif diff < 0:
        change_type = "decrease"
    else:
        change_type = "no_change"

    return {
        "old_value": old,
        "new_value": new,
        "difference": abs(diff),
        "percentage": abs(pct),
        "type": change_type,
    }


def percentage_difference(
    val_a: Union[int, float, str, Decimal],
    val_b: Union[int, float, str, Decimal],
) -> Decimal:
    """Calculate percentage difference between two values.
    
    Formula: (|A - B| / ((A + B) / 2)) * 100
    """
    a = _to_decimal(val_a)
    b = _to_decimal(val_b)
    avg = (a + b) / Decimal("2")
    if avg == 0:
        return Decimal("0")
    return _round_clean((abs(a - b) / abs(avg)) * Decimal("100"), places=2)


def simplify_ratio(a: int, b: int) -> Tuple[int, int]:
    """Simplify an integer ratio A : B to lowest terms."""
    if b == 0:
        raise ZeroDivisionError("Ratio denominator cannot be zero")
    g = math.gcd(int(a), int(b))
    return int(a // g), int(b // g)


def fraction_to_percentage(numerator: Union[int, float], denominator: Union[int, float]) -> Decimal:
    """Convert fraction N/D to percentage."""
    if denominator == 0:
        raise ZeroDivisionError("Denominator cannot be zero")
    n = _to_decimal(numerator)
    d = _to_decimal(denominator)
    return _round_clean((n / d) * Decimal("100"), places=2)


def percentage_to_decimal(percent: Union[int, float, str, Decimal]) -> Decimal:
    """Convert X% to decimal fraction."""
    p = _to_decimal(percent)
    return _round_clean(p / Decimal("100"), places=4)


def decimal_to_percentage(decimal_val: Union[int, float, str, Decimal]) -> Decimal:
    """Convert decimal value to percentage."""
    d = _to_decimal(decimal_val)
    return _round_clean(d * Decimal("100"), places=2)
