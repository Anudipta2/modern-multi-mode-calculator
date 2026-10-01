"""Business and Financial Calculator controller module."""

from typing import Dict, Any
from core.constants import CURRENCIES, DEFAULT_CURRENCY
from core.formatter import format_currency
from finance.gst import calculate_gst_add, calculate_gst_remove
from finance.profit_loss import calculate_profit_loss, calculate_selling_price_from_profit_percent
from finance.discount import calculate_discount, calculate_discount_from_prices
from finance.interest import calculate_simple_interest, calculate_compound_interest
from finance.emi import calculate_emi
from finance.ratios import (
    percentage_of,
    percentage_change,
    percentage_difference,
    simplify_ratio,
    fraction_to_percentage,
    percentage_to_decimal,
    decimal_to_percentage,
)


class BusinessCalculatorEngine:
    """Coordinates business calculations and formatting with multi-currency support."""

    def __init__(self, currency_code: str = DEFAULT_CURRENCY):
        self.currency_code = currency_code
        self.currency_symbol = CURRENCIES.get(currency_code, {}).get("symbol", "₹")

    def set_currency(self, currency_code: str) -> None:
        if currency_code in CURRENCIES:
            self.currency_code = currency_code
            self.currency_symbol = CURRENCIES[currency_code]["symbol"]

    def get_currency_symbol(self) -> str:
        return self.currency_symbol

    def format_money(self, amount, decimals=2) -> str:
        return format_currency(
            amount,
            currency_symbol=self.currency_symbol,
            decimals=decimals,
            use_indian=(self.currency_code == "INR"),
        )

    # --- Tool Computations ---
    def compute_gst_add(self, base_price, gst_rate, is_interstate=False) -> Dict[str, Any]:
        res = calculate_gst_add(base_price, gst_rate, is_interstate)
        return {
            **res,
            "fmt_base_price": self.format_money(res["base_price"]),
            "fmt_gst_amount": self.format_money(res["gst_amount"]),
            "fmt_final_price": self.format_money(res["final_price"]),
            "fmt_cgst": self.format_money(res["cgst"]),
            "fmt_sgst": self.format_money(res["sgst"]),
            "fmt_igst": self.format_money(res["igst"]),
        }

    def compute_gst_remove(self, final_price, gst_rate, is_interstate=False) -> Dict[str, Any]:
        res = calculate_gst_remove(final_price, gst_rate, is_interstate)
        return {
            **res,
            "fmt_base_price": self.format_money(res["base_price"]),
            "fmt_gst_amount": self.format_money(res["gst_amount"]),
            "fmt_final_price": self.format_money(res["final_price"]),
            "fmt_cgst": self.format_money(res["cgst"]),
            "fmt_sgst": self.format_money(res["sgst"]),
            "fmt_igst": self.format_money(res["igst"]),
        }

    def compute_profit_loss(self, cost_price, selling_price) -> Dict[str, Any]:
        res = calculate_profit_loss(cost_price, selling_price)
        return {
            **res,
            "fmt_cost_price": self.format_money(res["cost_price"]),
            "fmt_selling_price": self.format_money(res["selling_price"]),
            "fmt_amount": self.format_money(res["amount"]),
            "fmt_percentage": f"{res['percentage']}%",
        }

    def compute_discount(self, marked_price, discount_percent) -> Dict[str, Any]:
        res = calculate_discount(marked_price, discount_percent)
        return {
            **res,
            "fmt_marked_price": self.format_money(res["marked_price"]),
            "fmt_discount_amount": self.format_money(res["discount_amount"]),
            "fmt_final_price": self.format_money(res["final_price"]),
            "fmt_discount_percent": f"{res['discount_percent']}%",
        }

    def compute_simple_interest(self, principal, rate, time_val, time_unit="years") -> Dict[str, Any]:
        res = calculate_simple_interest(principal, rate, time_val, time_unit)
        return {
            **res,
            "fmt_principal": self.format_money(res["principal"]),
            "fmt_interest": self.format_money(res["interest"]),
            "fmt_total_amount": self.format_money(res["total_amount"]),
        }

    def compute_compound_interest(self, principal, rate, time_years, frequency="Annually") -> Dict[str, Any]:
        res = calculate_compound_interest(principal, rate, time_years, frequency)
        return {
            **res,
            "fmt_principal": self.format_money(res["principal"]),
            "fmt_interest": self.format_money(res["interest"]),
            "fmt_total_amount": self.format_money(res["total_amount"]),
        }

    def compute_emi(self, principal, rate, tenure, tenure_unit="years") -> Dict[str, Any]:
        res = calculate_emi(principal, rate, tenure, tenure_unit)
        return {
            **res,
            "fmt_principal": self.format_money(res["principal"]),
            "fmt_monthly_emi": self.format_money(res["monthly_emi"]),
            "fmt_total_interest": self.format_money(res["total_interest"]),
            "fmt_total_payable": self.format_money(res["total_payable"]),
        }

    def compute_percentage_of(self, percent, total_val) -> Dict[str, Any]:
        res = percentage_of(percent, total_val)
        return {"result": res, "fmt_result": f"{res:,}"}

    def compute_percentage_change(self, old_val, new_val) -> Dict[str, Any]:
        res = percentage_change(old_val, new_val)
        return {
            **res,
            "fmt_difference": f"{res['difference']:,}",
            "fmt_percentage": f"{res['percentage']}%",
        }

    def compute_simplify_ratio(self, a, b) -> Dict[str, Any]:
        num, den = simplify_ratio(a, b)
        return {"simplified_ratio": f"{num} : {den}", "numerator": num, "denominator": den}
