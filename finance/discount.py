"""Discount calculation module using Decimal."""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Union


def _to_decimal(val: Union[int, float, str, Decimal]) -> Decimal:
    if isinstance(val, Decimal):
        return val
    cleaned = str(val).replace(",", "").replace("%", "").strip()
    return Decimal(cleaned) if cleaned else Decimal("0")


def _round_currency(val: Decimal) -> Decimal:
    return val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _round_percent(val: Decimal) -> Decimal:
    return val.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def calculate_discount(
    marked_price: Union[int, float, str, Decimal],
    discount_percent: Union[int, float, str, Decimal],
) -> Dict[str, Decimal]:
    """Calculate discount amount and final selling price.
    
    Formula:
        Discount Amount = Marked Price * (Discount % / 100)
        Final Price = Marked Price - Discount Amount
    """
    mp = _to_decimal(marked_price)
    dp = _to_decimal(discount_percent)

    if mp < 0 or dp < 0:
        raise ValueError("Marked price and discount percent cannot be negative")

    discount_amount = _round_currency(mp * (dp / Decimal("100")))
    final_price = _round_currency(mp - discount_amount)

    return {
        "marked_price": _round_currency(mp),
        "discount_percent": dp,
        "discount_amount": discount_amount,
        "final_price": final_price,
    }


def calculate_discount_from_prices(
    marked_price: Union[int, float, str, Decimal],
    final_price: Union[int, float, str, Decimal],
) -> Dict[str, Decimal]:
    """Calculate discount percentage from marked and final selling price."""
    mp = _to_decimal(marked_price)
    fp = _to_decimal(final_price)

    if mp <= 0:
        raise ValueError("Marked price must be greater than zero")
    if fp < 0 or fp > mp:
        raise ValueError("Final price must be positive and not exceed marked price")

    discount_amount = _round_currency(mp - fp)
    discount_percent = _round_percent((discount_amount / mp) * Decimal("100"))

    return {
        "marked_price": _round_currency(mp),
        "final_price": _round_currency(fp),
        "discount_amount": discount_amount,
        "discount_percent": discount_percent,
    }
