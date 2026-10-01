"""Standard Calculator state engine."""

from typing import Tuple, Optional
from core.expression_parser import ExpressionEvaluator
from core.formatter import format_number


class StandardCalculatorEngine:
    """State machine for standard calculator operations."""

    def __init__(self, evaluator: Optional[ExpressionEvaluator] = None):
        self.evaluator = evaluator or ExpressionEvaluator()
        self.expression: str = ""       # Smaller expression/history line (e.g. "125 × 24 + 50")
        self.display_value: str = "0"   # Large current-value line (e.g. "3,050")
        self.memory: float = 0.0
        self.has_memory: bool = False
        self.is_new_entry: bool = True  # True if next digit replaces current display
        self.has_error: bool = False
        self.last_op_repeat: Optional[Tuple[str, str]] = None  # (operator, operand) for repeated equals

    def get_display(self) -> str:
        """Get formatted display value for UI."""
        if self.has_error:
            return self.display_value
        return format_number(self.display_value)

    def get_raw_display(self) -> str:
        return self.display_value

    def get_expression(self) -> str:
        """Get current expression line."""
        return self.expression

    def input_digit(self, digit: str) -> None:
        """Handle digit input (0-9)."""
        if self.has_error:
            self.clear_all()

        if self.is_new_entry:
            self.display_value = digit
            self.is_new_entry = False
        else:
            if self.display_value == "0":
                self.display_value = digit
            else:
                # Prevent unreasonable length
                if len(self.display_value) < 20:
                    self.display_value += digit

        self.last_op_repeat = None

    def input_decimal(self) -> None:
        """Handle decimal point input."""
        if self.has_error:
            self.clear_all()

        if self.is_new_entry:
            self.display_value = "0."
            self.is_new_entry = False
        else:
            if "." not in self.display_value:
                self.display_value += "."

    def input_operator(self, op: str) -> None:
        """Handle binary operators: +, −, ×, ÷, %"""
        if self.has_error:
            self.clear_all()

        # Map operator to visual glyph
        op_map = {"+": "+", "-": "−", "−": "−", "*": "×", "×": "×", "/": "÷", "÷": "÷", "%": "%"}
        glyph = op_map.get(op, op)

        if self.is_new_entry and self.expression and self.expression[-1] in ("+", "−", "×", "÷"):
            # Replace previous operator if user changed mind
            self.expression = self.expression[:-2].rstrip() + f" {glyph}"
            return

        if not self.expression:
            self.expression = f"{self.display_value} {glyph}"
        else:
            self.expression += f" {self.display_value} {glyph}"

        self.is_new_entry = True
        self.last_op_repeat = None

    def input_parenthesis(self, paren: str) -> None:
        """Handle ( or )."""
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

    def calculate(self) -> Tuple[bool, str]:
        """Perform evaluation (pressing '=').
        
        Returns:
            Tuple[bool, str]: (is_success, result_str)
        """
        if self.has_error:
            return False, self.display_value

        # Handle repeated equals (e.g. 5 + 2 = 7, then pressing = again gives 9)
        if self.expression.endswith("=") and self.last_op_repeat:
            op, operand = self.last_op_repeat
            expr_to_eval = f"{self.display_value} {op} {operand}"
        else:
            if not self.expression:
                return True, self.display_value

            # Extract last operator and operand for repeated equals before consuming
            tokens = self.expression.strip().split()
            if len(tokens) >= 2 and tokens[-1] in ("+", "−", "×", "÷"):
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
        """Delete last entered digit or character."""
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
        """Toggle ± (negate current display value)."""
        if self.has_error:
            return

        if self.display_value == "0":
            return

        if self.display_value.startswith("-"):
            self.display_value = self.display_value[1:]
        else:
            self.display_value = "-" + self.display_value

    def percentage(self) -> None:
        """Calculate percentage of current entry."""
        if self.has_error:
            return
        try:
            val = float(self.display_value)
            res = val / 100.0
            if res.is_integer():
                self.display_value = str(int(res))
            else:
                self.display_value = str(round(res, 10))
            self.is_new_entry = True
        except ValueError:
            pass

    def clear_all(self) -> None:
        """AC - clear everything."""
        self.expression = ""
        self.display_value = "0"
        self.is_new_entry = True
        self.has_error = False
        self.last_op_repeat = None

    def clear_entry(self) -> None:
        """C - clear current input only."""
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
