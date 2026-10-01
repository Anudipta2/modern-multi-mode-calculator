"""Scientific Calculator state engine."""

import math
import random
from typing import Tuple, Optional
from core.expression_parser import ExpressionEvaluator
from core.formatter import format_number
from core.constants import ANGLE_DEG, ANGLE_RAD, ANGLE_GRAD, PI, E, PHI


class ScientificCalculatorEngine:
    """State machine for scientific calculator operations."""

    def __init__(self):
        self.angle_mode: str = ANGLE_DEG
        self.evaluator = ExpressionEvaluator(angle_mode=self.angle_mode)
        self.expression: str = ""
        self.display_value: str = "0"
        self.memory: float = 0.0
        self.has_memory: bool = False
        self.is_new_entry: bool = True
        self.has_error: bool = False
        self.is_second_f: bool = False  # 2nd function toggle for inverse trig/powers
        self.last_op_repeat: Optional[Tuple[str, str]] = None

    def set_angle_mode(self, mode: str) -> None:
        """Set angle mode (DEG, RAD, GRAD)."""
        if mode in (ANGLE_DEG, ANGLE_RAD, ANGLE_GRAD):
            self.angle_mode = mode
            self.evaluator.set_angle_mode(mode)

    def toggle_angle_mode(self) -> str:
        """Cycle through DEG -> RAD -> GRAD -> DEG."""
        modes = [ANGLE_DEG, ANGLE_RAD, ANGLE_GRAD]
        idx = (modes.index(self.angle_mode) + 1) % len(modes)
        self.set_angle_mode(modes[idx])
        return self.angle_mode

    def toggle_second_f(self) -> bool:
        """Toggle 2nd function state (e.g., sin -> asin)."""
        self.is_second_f = not self.is_second_f
        return self.is_second_f

    def get_display(self) -> str:
        if self.has_error:
            return self.display_value
        return format_number(self.display_value)

    def get_raw_display(self) -> str:
        return self.display_value

    def get_expression(self) -> str:
        return self.expression

    def input_digit(self, digit: str) -> None:
        if self.has_error:
            self.clear_all()

        if self.is_new_entry:
            self.display_value = digit
            self.is_new_entry = False
        else:
            if self.display_value == "0":
                self.display_value = digit
            else:
                if len(self.display_value) < 25:
                    self.display_value += digit
        self.last_op_repeat = None

    def input_decimal(self) -> None:
        if self.has_error:
            self.clear_all()

        if self.is_new_entry:
            self.display_value = "0."
            self.is_new_entry = False
        else:
            if "." not in self.display_value:
                self.display_value += "."

    def input_constant(self, const_name: str) -> None:
        """Insert mathematical constant: pi, e, phi."""
        if self.has_error:
            self.clear_all()

        const_map = {"pi": PI, "π": PI, "e": E, "phi": PHI, "φ": PHI}
        val = const_map.get(const_name.lower(), PI)
        self.display_value = str(round(val, 12))
        self.is_new_entry = True
        self.last_op_repeat = None

    def input_operator(self, op: str) -> None:
        """Handle binary operators: +, −, ×, ÷, ^ (pow), %, nPr, nCr"""
        if self.has_error:
            self.clear_all()

        op_map = {
            "+": "+",
            "-": "−",
            "−": "−",
            "*": "×",
            "×": "×",
            "/": "÷",
            "÷": "÷",
            "^": "^",
            "%": "%",
            "nPr": "P",
            "nCr": "C",
        }
        glyph = op_map.get(op, op)

        if not self.expression:
            self.expression = f"{self.display_value} {glyph}"
        else:
            self.expression += f" {self.display_value} {glyph}"

        self.is_new_entry = True
        self.last_op_repeat = None

    def input_parenthesis(self, paren: str) -> None:
        if self.has_error:
            self.clear_all()

        if paren == "(":
            if self.is_new_entry:
                self.expression += " ("
            else:
                self.expression += f" {self.display_value} × ("
            self.display_value = "0"
            self.is_new_entry = True
        elif paren == ")":
            if not self.is_new_entry:
                self.expression += f" {self.display_value}"
            self.expression += " )"
            self.is_new_entry = True

    def apply_unary_function(self, func_name: str) -> None:
        """Apply an immediate mathematical unary function to the current entry.
        
        Examples:
            sin, cos, tan, cot, sec, csc,
            asin, acos, atan,
            sinh, cosh, tanh,
            sqrt, cbrt, x^2, x^3, 1/x, 10^x, e^x,
            ln, log10, abs, factorial, floor, ceil
        """
        if self.has_error:
            self.clear_all()

        current_val = self.display_value

        # Wrap in expression syntax for safe evaluation
        if func_name in ("sqr", "square", "x^2"):
            expr = f"({current_val})^2"
        elif func_name in ("cube", "x^3"):
            expr = f"({current_val})^3"
        elif func_name in ("recip", "1/x"):
            expr = f"1 / ({current_val})"
        elif func_name in ("sqrt", "√"):
            expr = f"sqrt({current_val})"
        elif func_name in ("cbrt", "∛"):
            expr = f"cbrt({current_val})"
        elif func_name in ("10^x", "10x"):
            expr = f"10^({current_val})"
        elif func_name in ("e^x", "ex"):
            expr = f"e^({current_val})"
        elif func_name in ("2^x",):
            expr = f"2^({current_val})"
        elif func_name in ("fact", "n!", "factorial"):
            expr = f"factorial({current_val})"
        elif func_name == "abs":
            expr = f"abs({current_val})"
        elif func_name == "floor":
            expr = f"floor({current_val})"
        elif func_name == "ceil":
            expr = f"ceil({current_val})"
        elif func_name == "rand":
            rand_val = round(random.random(), 6)
            self.display_value = str(rand_val)
            self.is_new_entry = True
            return
        elif func_name == "EE":
            # Scientific notation entry (e.g. 1.5e6)
            if "e" not in self.display_value.lower():
                self.display_value += "e"
                self.is_new_entry = False
            return
        else:
            # Standard function name: sin, cos, tan, etc.
            expr = f"{func_name}({current_val})"

        success, result = self.evaluator.evaluate(expr)
        if success:
            self.display_value = str(result)
            self.is_new_entry = True
            self.has_error = False
        else:
            self.has_error = True
            self.display_value = str(result)

    def calculate(self) -> Tuple[bool, str]:
        """Perform evaluation (pressing '=')."""
        if self.has_error:
            return False, self.display_value

        if self.expression.endswith("=") and self.last_op_repeat:
            op, operand = self.last_op_repeat
            expr_to_eval = f"{self.display_value} {op} {operand}"
        else:
            if not self.expression:
                return True, self.display_value

            tokens = self.expression.strip().split()
            if len(tokens) >= 2 and tokens[-1] in ("+", "−", "×", "÷", "^", "%", "P", "C"):
                self.last_op_repeat = (tokens[-1], self.display_value)

            if not self.is_new_entry:
                expr_to_eval = f"{self.expression} {self.display_value}"
            else:
                expr_to_eval = self.expression.rstrip(" =")

        success, result = self.evaluator.evaluate(expr_to_eval)
        if success:
            self.expression = f"{expr_to_eval} ="
            self.display_value = str(result)
            self.is_new_entry = True
            self.has_error = False
            return True, self.display_value
        else:
            self.has_error = True
            self.display_value = str(result)
            return False, self.display_value

    def backspace(self) -> None:
        if self.has_error or self.is_new_entry:
            self.display_value = "0"
            self.is_new_entry = True
            self.has_error = False
            return

        if len(self.display_value) > 1:
            self.display_value = self.display_value[:-1]
            if self.display_value in ("-", "-0"):
                self.display_value = "0"
                self.is_new_entry = True
        else:
            self.display_value = "0"
            self.is_new_entry = True

    def toggle_sign(self) -> None:
        if self.has_error or self.display_value == "0":
            return
        if self.display_value.startswith("-"):
            self.display_value = self.display_value[1:]
        else:
            self.display_value = "-" + self.display_value

    def clear_all(self) -> None:
        self.expression = ""
        self.display_value = "0"
        self.is_new_entry = True
        self.has_error = False
        self.last_op_repeat = None

    def clear_entry(self) -> None:
        self.display_value = "0"
        self.is_new_entry = True
        self.has_error = False

    # --- Memory Operations ---
    def memory_clear(self) -> None:
        self.memory = 0.0
        self.has_memory = False

    def memory_recall(self) -> None:
        if self.has_memory:
            if float(self.memory).is_integer():
                self.display_value = str(int(self.memory))
            else:
                self.display_value = str(self.memory)
            self.is_new_entry = True

    def memory_add(self) -> None:
        try:
            val = float(self.display_value)
            self.memory += val
            self.has_memory = True
            self.is_new_entry = True
        except ValueError:
            pass

    def memory_subtract(self) -> None:
        try:
            val = float(self.display_value)
            self.memory -= val
            self.has_memory = True
            self.is_new_entry = True
        except ValueError:
            pass

    def memory_store(self) -> None:
        try:
            self.memory = float(self.display_value)
            self.has_memory = True
            self.is_new_entry = True
        except ValueError:
            pass
