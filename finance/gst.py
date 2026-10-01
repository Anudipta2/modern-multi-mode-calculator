"""Goods and Services Tax (GST) calculator module using Decimal for financial precision."""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Union


def _to_decimal(val: Union[int, float, str, Decimal]) -> Decimal:
    if isinstance(val, Decimal):
        return val
    cleaned = str(val).replace(",", "").replace("%", "").strip()
    return Decimal(cleaned) if cleaned else Decimal("0")


def _round_currency(val: Decimal) -> Decimal:
    return val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_gst_add(
    base_price: Union[int, float, str, Decimal],
    gst_rate: Union[int, float, str, Decimal],
    is_interstate: bool = False,
) -> Dict[str, Decimal]:
    """Calculate GST added to base price.
    
    Formula:
        GST Amount = Base Price * (GST Rate / 100)
        Final Price = Base Price + GST Amount
        Intra-state: CGST = SGST = GST Amount / 2
        Inter-state: IGST = GST Amount
    """
    bp = _to_decimal(base_price)
    rate = _to_decimal(gst_rate)

    if bp < 0 or rate < 0:
        raise ValueError("Price and GST rate cannot be negative")

    gst_amount = _round_currency(bp * (rate / Decimal("100")))
    final_price = _round_currency(bp + gst_amount)

    if is_interstate:
        cgst = Decimal("0.00")
        sgst = Decimal("0.00")
        igst = gst_amount
    else:
        cgst = _round_currency(gst_amount / Decimal("2"))
        sgst = _round_currency(gst_amount - cgst)  # Handles 1 cent rounding discrepancy
        igst = Decimal("0.00")

    return {
        "base_price": _round_currency(bp),
        "gst_rate": rate,
        "gst_amount": gst_amount,
        "final_price": final_price,
        "cgst": cgst,
        "sgst": sgst,
        "igst": igst,
        "is_interstate": is_interstate,
    }


def calculate_gst_remove(
    final_price: Union[int, float, str, Decimal],
    gst_rate: Union[int, float, str, Decimal],
    is_interstate: bool = False,
) -> Dict[str, Decimal]:
    """Calculate base price and GST component from gross (inclusive) price.
    
    Formula:
        Base Price = Final Price / (1 + GST Rate / 100)
        GST Amount = Final Price - Base Price
    """
    fp = _to_decimal(final_price)
    rate = _to_decimal(gst_rate)

    if fp < 0 or rate < 0:
        raise ValueError("Price and GST rate cannot be negative")

    divisor = Decimal("1") + (rate / Decimal("100"))
    base_price = _round_currency(fp / divisor)
    gst_amount = _round_currency(fp - base_price)

    if is_interstate:
        cgst = Decimal("0.00")
        sgst = Decimal("0.00")
        igst = gst_amount
    else:
        cgst = _round_currency(gst_amount / Decimal("2"))
        sgst = _round_currency(gst_amount - cgst)
        igst = Decimal("0.00")

    return {
        "base_price": base_price,
        "gst_rate": rate,
        "gst_amount": gst_amount,
        "final_price": _round_currency(fp),
        "cgst": cgst,
        "sgst": sgst,
        "igst": igst,
        "is_interstate": is_interstate,
    }
