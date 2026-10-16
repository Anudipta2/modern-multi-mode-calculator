"""Extreme data fuzzing & critical vulnerability test suite."""

import sys
import math
import os
from decimal import Decimal

sys.path.insert(0, r"c:\Users\anudi\OneDrive\Documents\ModernCalculator")

from core.expression_parser import ExpressionEvaluator
from core.formatter import format_number, format_currency
from calculators.standard import StandardCalculatorEngine
from calculators.scientific import ScientificCalculatorEngine
from calculators.business import BusinessCalculatorEngine
from core.history import HistoryManager

ev = ExpressionEvaluator()

print("=" * 65)
print("EXTREME CRITICAL TESTING: EXPRESSIONS & AST PARSER")
print("=" * 65)

extreme_expressions = [
    # Subnormal and astronomical numbers
    "1e-320",
    "1e300 * 1e8",
    "1e300 * 1e300",
    "1 / 1e-320",
    "0 ** 0",
    "0 ** 5",
    "0 ** -2",
    "(-0.0) + 0",
    "-(-(-(-5)))",
    # Advanced Combinatorics Edge Cases
    "nPr(0, 0)",
    "nCr(0, 0)",
    "nPr(10, 0)",
    "nCr(10, 0)",
    "nPr(5, 5)",
    "nCr(5, 5)",
    "nPr(5, 6)",        # r > n
    "nCr(5, 6)",        # r > n
    "nPr(-5, 2)",       # negative n
    "nCr(5, -2)",       # negative r
    "nPr(5.5, 2)",      # non-integer
    "nCr(5, 2.5)",      # non-integer
    "nPr(1000000, 2)",  # massive permutation
    "nCr(1000000, 2)",  # massive combination
    # Extreme factorials
    "0!",
    "1!",
    "0.0!",
    "1.0!",
    "(-0.0)!",
    # Extreme Logarithms
    "log(0)",
    "log(-5)",
    "log(1e-300)",
    "log(10, 1)",       # base == 1 invalid
    "log(10, 0)",       # base == 0 invalid
    "log(10, -2)",      # negative base
    "ln(0)",
    "ln(-1)",
    "ln(1)",
    "ln(e)",
    # Trigonometry edge cases
    "sin(0)",
    "cos(0)",
    "tan(0)",
    "atan(0)",
    "atan(1e300)",
    "asin(1)",
    "asin(-1)",
    "acos(1)",
    "acos(-1)",
    "sinh(0)",
    "cosh(0)",
    "tanh(0)",
    "asinh(0)",
    "acosh(1)",
    "acosh(0.999999)",   # domain error < 1
    "atanh(0)",
    "atanh(1)",          # asymptote 1
    "atanh(-1)",         # asymptote -1
    "atanh(1.0001)",     # domain error
    # Unicode and symbol normalization
    "π + φ",
    "2π",
    "3φ",
    "2(3)(4)",
    "(2+3)(4+5)",
    "√144",
    "√(144)",
    "10P3",
    "10C3",
    "10 p 3",
    "10 c 3",
    # Consecutive operations & weird formatting
    "5 + - 3",
    "5 - - 3",
    "5 * + 3",
    "5 / + 3",
    # Modulo variations
    "15 mod 4",
    "15 mod 0",
    "0 mod 5",
    "(-15) mod 4",
    # Extreme percentages
    "0%",
    "0 + 0%",
    "100 + 0%",
    "0 + 100%",
    "100 - 100%",
    "100 * 0%",
]

for expr in extreme_expressions:
    try:
        ok, res = ev.evaluate(expr)
        status = "PASS" if ok else "HANDLED"
        print(f"[{status:<7}] {expr:<25} -> {str(res)[:45]}")
    except Exception as e:
        print(f"[CRASH  ] {expr:<25} -> {type(e).__name__}: {e}")

print("\n" + "=" * 65)
print("EXTREME CRITICAL TESTING: ENGINE STATE MACHINES")
print("=" * 65)

# Standard Engine Fuzzing
std = StandardCalculatorEngine()
try:
    # 1. Repeated equals after error
    std.input_digit("5")
    std.input_operator("÷")
    std.input_digit("0")
    std.calculate()
    for _ in range(5):
        std.calculate()
    print("[PASS   ] Repeated equals after zero division: handled cleanly")
except Exception as e:
    print(f"[CRASH  ] Standard repeated equals: {e}")

try:
    # 2. Backspace fuzzing
    std.clear_all()
    std.backspace()
    std.backspace()
    std.input_digit("5")
    std.toggle_sign()
    std.backspace()
    assert std.display_value in ("0", "-0", "")
    print("[PASS   ] Backspace from negative single digit: handled cleanly")
except Exception as e:
    print(f"[CRASH  ] Standard backspace: {e}")

# Scientific Engine Fuzzing
sci = ScientificCalculatorEngine()
try:
    # Unary functions on 0
    sci.clear_all()
    sci.apply_unary_function("1/x")
    print(f"[PASS   ] 1/0 unary function: {sci.display_value}")
except Exception as e:
    print(f"[CRASH  ] Scientific 1/0: {e}")

try:
    # Unary functions on negative numbers
    sci.clear_all()
    sci.input_digit("4")
    sci.toggle_sign()
    sci.apply_unary_function("sqrt")
    print(f"[PASS   ] sqrt(-4) unary function: {sci.display_value}")
except Exception as e:
    print(f"[CRASH  ] Scientific sqrt(-4): {e}")

try:
    # Memory store with invalid values
    sci.display_value = "Error"
    sci.memory_store()
    sci.display_value = "Infinity"
    sci.memory_add()
    print(f"[PASS   ] Memory store on Error/Inf: memory={sci.memory}")
except Exception as e:
    print(f"[CRASH  ] Scientific memory store: {e}")

print("\n" + "=" * 65)
print("EXTREME CRITICAL TESTING: BUSINESS ENGINE")
print("=" * 65)

biz = BusinessCalculatorEngine()

extreme_biz_cases = [
    # Zero amounts
    ("GST 0 amount", lambda: biz.compute_gst_add("0", "18")),
    ("GST 0 rate", lambda: biz.compute_gst_add("1000", "0")),
    ("Discount 0 marked", lambda: biz.compute_discount("0", "15")),
    ("Discount 0 percent", lambda: biz.compute_discount("1000", "0")),
    ("Discount 100 percent", lambda: biz.compute_discount("1000", "100")),
    ("P&L 0 cost 0 sell", lambda: biz.compute_profit_loss("0", "0")),
    ("P&L 0 cost 100 sell", lambda: biz.compute_profit_loss("0", "100")),
    ("P&L 100 cost 0 sell", lambda: biz.compute_profit_loss("100", "0")),
    ("EMI 0 interest", lambda: biz.compute_emi("100000", "0", "1")),
    ("SI 0 rate", lambda: biz.compute_simple_interest("1000", "0", "1")),
    ("CI 0 rate", lambda: biz.compute_compound_interest("1000", "0", "1")),
    ("Ratio 0 to 5", lambda: biz.compute_simplify_ratio(0, 5)),
    ("Ratio 5 to 5", lambda: biz.compute_simplify_ratio(5, 5)),
    ("Ratio -5 to 10", lambda: biz.compute_simplify_ratio(-5, 10)),
    # Astronomical amounts
    ("GST 10^15 amount", lambda: biz.compute_gst_add("1000000000000000", "18")),
    ("Discount 10^15 marked", lambda: biz.compute_discount("1000000000000000", "10")),
    ("EMI 10^12 amount", lambda: biz.compute_emi("1000000000000", "8.5", "30")),
]

for name, fn in extreme_biz_cases:
    try:
        res = fn()
        print(f"[PASS   ] {name:<25} -> OK")
    except Exception as e:
        print(f"[CRASH  ] {name:<25} -> {type(e).__name__}: {e}")
