"""Profit and Loss calculation module using Decimal."""

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


def calculate_profit_loss(
    cost_price: Union[int, float, str, Decimal],
    selling_price: Union[int, float, str, Decimal],
) -> Dict[str, Union[Decimal, str]]:
    """Calculate profit or loss and corresponding percentage from CP and SP.
    
    Returns a dict with:
        cost_price, selling_price, difference, status ('profit', 'loss', 'breakeven'),
        percentage.
    """
    cp = _to_decimal(cost_price)
    sp = _to_decimal(selling_price)

    if cp < 0 or sp < 0:
        raise ValueError("Cost price and selling price cannot be negative")

    diff = sp - cp

    if diff > 0:
        status = "profit"
        profit_amount = diff
        profit_percent = (
            _round_percent((profit_amount / cp) * Decimal("100"))
            if cp > 0
            else Decimal("100")
        )
        return {
            "cost_price": _round_currency(cp),
            "selling_price": _round_currency(sp),
            "amount": _round_currency(profit_amount),
            "percentage": profit_percent,
            "status": status,
        }
    elif diff < 0:
        status = "loss"
        loss_amount = abs(diff)
        loss_percent = (
            _round_percent((loss_amount / cp) * Decimal("100"))
            if cp > 0
            else Decimal("0")
        )
        return {
            "cost_price": _round_currency(cp),
            "selling_price": _round_currency(sp),
            "amount": _round_currency(loss_amount),
            "percentage": loss_percent,
            "status": status,
        }
    else:
        return {
            "cost_price": _round_currency(cp),
            "selling_price": _round_currency(sp),
            "amount": Decimal("0.00"),
            "percentage": Decimal("0.00"),
            "status": "breakeven",
        }


def calculate_selling_price_from_profit_percent(
    cost_price: Union[int, float, str, Decimal],
    profit_percent: Union[int, float, str, Decimal],
) -> Dict[str, Decimal]:
    """Calculate selling price given cost price and target profit %."""
    cp = _to_decimal(cost_price)
    pct = _to_decimal(profit_percent)
    profit = cp * (pct / Decimal("100"))
    sp = cp + profit
    return {
        "cost_price": _round_currency(cp),
        "selling_price": _round_currency(sp),
        "profit": _round_currency(profit),
        "profit_percent": pct,
    }
