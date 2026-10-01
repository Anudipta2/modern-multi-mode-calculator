"""Number and currency formatting utilities for the Modern Calculator."""

from decimal import Decimal, InvalidOperation
import math


def format_number(val, max_digits=12, use_indian_grouping=False) -> str:
    """Format a numeric value (int, float, Decimal, str) cleanly for display.
    
    - Handles very large / very small numbers using scientific notation.
    - Removes trailing zeros after decimal point for non-integers if not fixed.
    - Adds thousands commas.
    """
    if val is None or val == "":
        return "0"
    
    if isinstance(val, str):
        val = val.strip().replace(",", "")
        if val in ("Error", "NaN", "Infinity", "-Infinity"):
            return val
        try:
            if "." in val or "e" in val.lower():
                val = float(val)
            else:
                val = int(val)
        except ValueError:
            return val

    # Check for NaN or Inf
    if isinstance(val, float):
        if math.isnan(val):
            return "Error"
        if math.isinf(val):
            return "Infinity" if val > 0 else "-Infinity"

    # Convert to float or int for magnitude check
    abs_val = abs(val)

    # Scientific notation for very large or tiny non-zero numbers
    if abs_val != 0 and (abs_val >= 1e15 or abs_val < 1e-6):
        return f"{val:.6e}".replace("e+0", "e+").replace("e-0", "e-")

    # Round to avoid float representation artifacts (e.g., 0.1 + 0.2 = 0.30000000000000004)
    if isinstance(val, float):
        # Round to 11 decimal places then strip trailing zeros
        rounded = round(val, 11)
        if rounded.is_integer():
            val = int(rounded)
        else:
            val = rounded

    if isinstance(val, int):
        if use_indian_grouping:
            return format_indian_grouping(val)
        return f"{val:,}"

    # For floats / Decimals:
    val_str = f"{val:.10f}".rstrip("0").rstrip(".")
    if "." in val_str:
        integer_part, decimal_part = val_str.split(".", 1)
        try:
            int_val = int(integer_part)
            if use_indian_grouping:
                formatted_int = format_indian_grouping(int_val)
            else:
                formatted_int = f"{int_val:,}"
            return f"{formatted_int}.{decimal_part}"
        except ValueError:
            return val_str
    else:
        try:
            int_val = int(val_str)
            if use_indian_grouping:
                return format_indian_grouping(int_val)
            return f"{int_val:,}"
        except ValueError:
            return val_str


def format_indian_grouping(num: int) -> str:
    """Format an integer with Indian comma grouping (e.g., 10,00,000)."""
    s = str(abs(num))
    if len(s) <= 3:
        res = s
    else:
        last3 = s[-3:]
        remaining = s[:-3]
        groups = []
        while len(remaining) > 2:
            groups.append(remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.append(remaining)
        groups.reverse()
        res = ",".join(groups) + "," + last3
    return f"-{res}" if num < 0 else res


def format_currency(amount, currency_symbol="₹", decimals=2, use_indian=True) -> str:
    """Format amount as currency string, e.g. ₹1,250.00"""
    try:
        if isinstance(amount, (str, int, float)):
            d = Decimal(str(amount).replace(",", "").strip())
        elif isinstance(amount, Decimal):
            d = amount
        else:
            return f"{currency_symbol}0.00"
    except (InvalidOperation, ValueError):
        return f"{currency_symbol}0.00"

    # Quantize to required decimals
    factor = Decimal("10") ** -decimals
    quantized = d.quantize(factor)

    parts = str(quantized).split(".")
    integer_part = int(parts[0])
    decimal_part = parts[1] if len(parts) > 1 else "00"

    if use_indian and currency_symbol == "₹":
        formatted_int = format_indian_grouping(integer_part)
    else:
        formatted_int = f"{integer_part:,}"

    if decimals > 0:
        return f"{currency_symbol}{formatted_int}.{decimal_part}"
    return f"{currency_symbol}{formatted_int}"


def parse_clean_decimal(val_str: str) -> Decimal:
    """Safely parse user-entered string into Decimal, handling currency symbols and commas."""
    if not val_str:
        return Decimal("0")
    cleaned = (
        str(val_str)
        .replace("₹", "")
        .replace("$", "")
        .replace("€", "")
        .replace("£", "")
        .replace("¥", "")
        .replace(",", "")
        .replace("%", "")
        .strip()
    )
    if not cleaned:
        return Decimal("0")
    return Decimal(cleaned)
