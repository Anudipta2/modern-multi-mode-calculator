"""Simple and Compound Interest calculation module using Decimal."""

from decimal import Decimal, ROUND_HALF_UP
import math
from typing import Dict, Union


def _to_decimal(val: Union[int, float, str, Decimal]) -> Decimal:
    if isinstance(val, Decimal):
        return val
    cleaned = str(val).replace(",", "").replace("%", "").strip()
    return Decimal(cleaned) if cleaned else Decimal("0")


def _round_currency(val: Decimal) -> Decimal:
    return val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_simple_interest(
    principal: Union[int, float, str, Decimal],
    rate: Union[int, float, str, Decimal],
    time_value: Union[int, float, str, Decimal],
    time_unit: str = "years",  # 'years', 'months', 'days'
) -> Dict[str, Decimal]:
    """Calculate Simple Interest.
    
    Formula:
        SI = (P * R * T) / 100
        Total = P + SI
    """
    p = _to_decimal(principal)
    r = _to_decimal(rate)
    t_val = _to_decimal(time_value)

    if p < 0 or r < 0 or t_val < 0:
        raise ValueError("Principal, rate, and time must be non-negative")

    unit = time_unit.lower()
    if unit == "months":
        t_years = t_val / Decimal("12")
    elif unit == "days":
        t_years = t_val / Decimal("365")
    else:
        t_years = t_val

    interest = _round_currency((p * r * t_years) / Decimal("100"))
    total_amount = _round_currency(p + interest)

    return {
        "principal": _round_currency(p),
        "rate": r,
        "time_years": t_years,
        "interest": interest,
        "total_amount": total_amount,
    }


def calculate_compound_interest(
    principal: Union[int, float, str, Decimal],
    rate: Union[int, float, str, Decimal],
    time_years: Union[int, float, str, Decimal],
    compounding_frequency: str = "Annually",
) -> Dict[str, Decimal]:
    """Calculate Compound Interest.
    
    Formula:
        A = P * (1 + R / (100 * n))^(n * T)
        CI = A - P
    """
    p = _to_decimal(principal)
    r = _to_decimal(rate)
    t = _to_decimal(time_years)

    if p < 0 or r < 0 or t < 0:
        raise ValueError("Principal, rate, and time must be non-negative")

    freq_map = {
        "annually": 1,
        "half-yearly": 2,
        "quarterly": 4,
        "monthly": 12,
        "daily": 365,
    }
    n = Decimal(str(freq_map.get(compounding_frequency.lower(), 1)))

    if p == 0 or r == 0 or t == 0:
        return {
            "principal": _round_currency(p),
            "rate": r,
            "time_years": t,
            "interest": Decimal("0.00"),
            "total_amount": _round_currency(p),
        }

    # Decimal high precision power calculation
    try:
        periodic_rate = (r / Decimal("100")) / n
        factor = Decimal("1") + periodic_rate
        total_periods = float(n * t)
        multiplier = Decimal(str(math.pow(float(factor), total_periods)))
        final_amount = _round_currency(p * multiplier)
        interest = _round_currency(final_amount - p)
    except OverflowError:
        raise OverflowError("Compound interest calculation produced an overflow")

    return {
        "principal": _round_currency(p),
        "rate": r,
        "time_years": t,
        "frequency": compounding_frequency,
        "interest": interest,
        "total_amount": final_amount,
    }
