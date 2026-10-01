"""Equated Monthly Installment (EMI) and Loan calculator module using Decimal."""

from decimal import Decimal, ROUND_HALF_UP
import math
from typing import Dict, List, Union


def _to_decimal(val: Union[int, float, str, Decimal]) -> Decimal:
    if isinstance(val, Decimal):
        return val
    cleaned = str(val).replace(",", "").replace("%", "").strip()
    return Decimal(cleaned) if cleaned else Decimal("0")


def _round_currency(val: Decimal) -> Decimal:
    return val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_emi(
    principal: Union[int, float, str, Decimal],
    annual_interest_rate: Union[int, float, str, Decimal],
    tenure: Union[int, float, str, Decimal],
    tenure_unit: str = "years",  # 'years' or 'months'
) -> Dict[str, Union[Decimal, List[Dict]]]:
    """Calculate standard reducing-balance Loan EMI.
    
    Formula:
        EMI = [P * r * (1+r)^N] / [(1+r)^N - 1]
        where r is monthly interest rate, N is tenure in months.
    """
    p = _to_decimal(principal)
    annual_rate = _to_decimal(annual_interest_rate)
    tenure_val = _to_decimal(tenure)

    if p <= 0:
        raise ValueError("Principal loan amount must be greater than zero")
    if annual_rate < 0 or tenure_val <= 0:
        raise ValueError("Interest rate and tenure must be positive numbers")

    # Determine total months
    if tenure_unit.lower() == "years":
        total_months = int(round(float(tenure_val * Decimal("12"))))
    else:
        total_months = int(round(float(tenure_val)))

    if total_months <= 0:
        raise ValueError("Tenure must be at least 1 month")

    # Zero interest loan edge case
    if annual_rate == 0:
        emi = _round_currency(p / Decimal(str(total_months)))
        total_payable = _round_currency(emi * Decimal(str(total_months)))
        return {
            "principal": _round_currency(p),
            "annual_rate": annual_rate,
            "tenure_months": total_months,
            "monthly_emi": emi,
            "total_interest": Decimal("0.00"),
            "total_payable": total_payable,
            "schedule_preview": [],
        }

    # Monthly rate r = Annual Rate / (12 * 100)
    monthly_r = float(annual_rate / Decimal("1200"))
    n = total_months

    try:
        factor = math.pow(1.0 + monthly_r, n)
        emi_float = float(p) * monthly_r * factor / (factor - 1.0)
        emi = _round_currency(Decimal(str(emi_float)))
        total_payable = _round_currency(emi * Decimal(str(n)))
        total_interest = _round_currency(total_payable - p)
    except OverflowError:
        raise OverflowError("EMI calculation produced a numerical overflow")

    # Generate first few months schedule preview
    preview = []
    balance = float(p)
    preview_count = min(12, total_months)
    for month in range(1, preview_count + 1):
        interest_part = balance * monthly_r
        principal_part = float(emi) - interest_part
        if principal_part > balance:
            principal_part = balance
        balance = max(0.0, balance - principal_part)
        preview.append({
            "month": month,
            "principal": round(principal_part, 2),
            "interest": round(interest_part, 2),
            "balance": round(balance, 2),
        })

    return {
        "principal": _round_currency(p),
        "annual_rate": annual_rate,
        "tenure_months": total_months,
        "monthly_emi": emi,
        "total_interest": total_interest,
        "total_payable": total_payable,
        "schedule_preview": preview,
    }
