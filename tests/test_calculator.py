"""Comprehensive unit tests for the Modern Calculator engines and financial modules."""

import pytest
import math
from decimal import Decimal
from core.expression_parser import ExpressionEvaluator
from core.constants import ANGLE_DEG, ANGLE_RAD, ANGLE_GRAD
from core.formatter import format_number, format_indian_grouping, format_currency
from calculators.standard import StandardCalculatorEngine
from calculators.scientific import ScientificCalculatorEngine
from finance.gst import calculate_gst_add, calculate_gst_remove
from finance.profit_loss import calculate_profit_loss
from finance.discount import calculate_discount
from finance.interest import calculate_simple_interest, calculate_compound_interest
from finance.emi import calculate_emi
from finance.ratios import (
    percentage_of,
    percentage_change,
    simplify_ratio,
    fraction_to_percentage,
)


# ==========================================
# 1. Standard Calculator Tests
# ==========================================
def test_standard_basic_arithmetic():
    evaluator = ExpressionEvaluator()

    # 2 + 2 = 4
    ok, res = evaluator.evaluate("2 + 2")
    assert ok and res == 4

    # 10 - 4 = 6
    ok, res = evaluator.evaluate("10 - 4")
    assert ok and res == 6

    # 5 * 6 = 30
    ok, res = evaluator.evaluate("5 * 6")
    assert ok and res == 30

    # 20 / 4 = 5
    ok, res = evaluator.evaluate("20 / 4")
    assert ok and res == 5


def test_standard_operator_precedence():
    evaluator = ExpressionEvaluator()
    # 2 + 3 * 4 must equal 14, not 20
    ok, res = evaluator.evaluate("2 + 3 * 4")
    assert ok and res == 14

    # Parentheses: (2 + 3) * 4 = 20
    ok, res = evaluator.evaluate("(2 + 3) * 4")
    assert ok and res == 20


def test_standard_engine_interaction():
    engine = StandardCalculatorEngine()
    # Type 1, 2, 5
    engine.input_digit("1")
    engine.input_digit("2")
    engine.input_digit("5")
    assert engine.get_raw_display() == "125"

    # Operator +
    engine.input_operator("+")
    assert engine.get_expression() == "125 +"

    # Type 7, 5
    engine.input_digit("7")
    engine.input_digit("5")
    assert engine.get_raw_display() == "75"

    # Equals =
    ok, res = engine.calculate()
    assert ok and res == "200"
    assert engine.get_display() == "200"


def test_standard_repeated_equals():
    engine = StandardCalculatorEngine()
    engine.input_digit("5")
    engine.input_operator("+")
    engine.input_digit("2")
    engine.calculate()
    assert engine.get_raw_display() == "7"

    # Repeated equals adds 2 again -> 9
    engine.calculate()
    assert engine.get_raw_display() == "9"

    # Repeated equals adds 2 again -> 11
    engine.calculate()
    assert engine.get_raw_display() == "11"


# ==========================================
# 2. Scientific Calculator Tests
# ==========================================
def test_scientific_functions():
    evaluator = ExpressionEvaluator(angle_mode=ANGLE_DEG)

    # sqrt(144) = 12
    ok, res = evaluator.evaluate("sqrt(144)")
    assert ok and res == 12

    # 2^10 = 1024
    ok, res = evaluator.evaluate("2^10")
    assert ok and res == 1024

    # sin(30°) = 0.5
    ok, res = evaluator.evaluate("sin(30)")
    assert ok and abs(res - 0.5) < 1e-9

    # cos(60°) = 0.5
    ok, res = evaluator.evaluate("cos(60)")
    assert ok and abs(res - 0.5) < 1e-9

    # tan(45°) = 1
    ok, res = evaluator.evaluate("tan(45)")
    assert ok and abs(res - 1.0) < 1e-9

    # log10(1000) = 3
    ok, res = evaluator.evaluate("log10(1000)")
    assert ok and res == 3

    # ln(e) = 1
    ok, res = evaluator.evaluate("ln(e)")
    assert ok and abs(res - 1.0) < 1e-9

    # 5! = 120
    ok, res = evaluator.evaluate("5!")
    assert ok and res == 120

    # Combinatorics: 10P3 = 720, 10C3 = 120
    ok, res = evaluator.evaluate("10P3")
    assert ok and res == 720

    ok, res = evaluator.evaluate("10C3")
    assert ok and res == 120


def test_scientific_angle_modes():
    # Radians mode
    eval_rad = ExpressionEvaluator(angle_mode=ANGLE_RAD)
    ok, res = eval_rad.evaluate(f"sin({math.pi / 6})")
    assert ok and abs(res - 0.5) < 1e-9

    # Gradians mode: 100 grads = 90 deg -> sin(100) = 1
    eval_grad = ExpressionEvaluator(angle_mode=ANGLE_GRAD)
    ok, res = eval_grad.evaluate("sin(100)")
    assert ok and abs(res - 1.0) < 1e-9


# ==========================================
# 3. Security & Error Handling Tests
# ==========================================
def test_safe_parser_blocks_arbitrary_code():
    evaluator = ExpressionEvaluator()
    dangerous_payloads = [
        "__import__('os').system('dir')",
        "open('test.txt', 'w')",
        "eval('2+2')",
        "exec('a = 5')",
        "import sys",
        "[x for x in (1, 2, 3)]",
        "lambda x: x + 1",
    ]
    for payload in dangerous_payloads:
        ok, res = evaluator.evaluate(payload)
        assert not ok, f"Security violation: payload '{payload}' was evaluated!"


def test_division_by_zero():
    evaluator = ExpressionEvaluator()
    ok, msg = evaluator.evaluate("10 / 0")
    assert not ok
    assert "divide by zero" in msg.lower()


# ==========================================
# 4. Business & Financial Tests
# ==========================================
def test_gst_calculations():
    # 18% GST on ₹1000 = ₹180, Total = ₹1180
    res_add = calculate_gst_add(1000, 18, is_interstate=False)
    assert res_add["gst_amount"] == Decimal("180.00")
    assert res_add["final_price"] == Decimal("1180.00")
    assert res_add["cgst"] == Decimal("90.00")
    assert res_add["sgst"] == Decimal("90.00")

    # Remove 18% GST from ₹1180 = ₹1000 base, ₹180 GST
    res_rem = calculate_gst_remove(1180, 18)
    assert res_rem["base_price"] == Decimal("1000.00")
    assert res_rem["gst_amount"] == Decimal("180.00")


def test_profit_and_loss():
    # ₹1000 cost and ₹1250 selling price = ₹250 profit (25%)
    res = calculate_profit_loss(1000, 1250)
    assert res["status"] == "profit"
    assert res["amount"] == Decimal("250.00")
    assert res["percentage"] == Decimal("25.0000")

    # ₹1000 cost and ₹800 selling price = ₹200 loss (20%)
    res_loss = calculate_profit_loss(1000, 800)
    assert res_loss["status"] == "loss"
    assert res_loss["amount"] == Decimal("200.00")
    assert res_loss["percentage"] == Decimal("20.0000")


def test_discount():
    # ₹2000 with 15% discount = ₹300 discount, ₹1700 final
    res = calculate_discount(2000, 15)
    assert res["discount_amount"] == Decimal("300.00")
    assert res["final_price"] == Decimal("1700.00")


def test_simple_interest():
    # P=10,000, R=10%, T=2 years -> SI=2,000, Total=12,000
    res = calculate_simple_interest(10000, 10, 2, "years")
    assert res["interest"] == Decimal("2000.00")
    assert res["total_amount"] == Decimal("12000.00")


def test_compound_interest():
    # P=10,000, R=10%, T=2 years compounded annually -> 10,000 * 1.21 = 12,100
    res = calculate_compound_interest(10000, 10, 2, "Annually")
    assert res["total_amount"] == Decimal("12100.00")
    assert res["interest"] == Decimal("2100.00")


def test_emi_calculation():
    # P=100,000, R=12% annual, T=1 year (12 months)
    res = calculate_emi(100000, 12, 1, "years")
    # Monthly EMI ~ ₹8,884.88
    assert res["monthly_emi"] == Decimal("8884.88")
    assert res["tenure_months"] == 12
    assert res["total_payable"] == Decimal("106618.56")
    assert res["total_interest"] == Decimal("6618.56")


def test_ratios_and_percentages():
    # 20% of 500 = 100
    assert percentage_of(20, 500) == Decimal("100.00")

    # Ratio simplification: 50 : 100 -> 1 : 2
    assert simplify_ratio(50, 100) == (1, 2)
    assert simplify_ratio(36, 48) == (3, 4)

    # Fraction 3/4 = 75%
    assert fraction_to_percentage(3, 4) == Decimal("75.00")


def test_formatters():
    assert format_number(1000) == "1,000"
    assert format_number(1000000) == "1,000,000"
    assert format_indian_grouping(1000000) == "10,00,000"
    assert format_currency(1250, "₹") == "₹1,250.00"
