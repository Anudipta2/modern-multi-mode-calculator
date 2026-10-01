"""Safe mathematical expression parser using Python AST.

Evaluates mathematical expressions without using unsafe unrestricted eval().
Adheres strictly to mathematical precedence, supports trigonometry, logarithms,
powers, roots, factorials, permutations, combinations, and angle modes.
"""

import ast
import math
import re
from typing import Any, Tuple, Union
from core.constants import PI, E, PHI, ANGLE_DEG, ANGLE_RAD, ANGLE_GRAD


class ExpressionEvaluator:
    """Safe AST-based mathematical expression evaluator."""

    def __init__(self, angle_mode: str = ANGLE_DEG):
        self.angle_mode = angle_mode

    def set_angle_mode(self, mode: str):
        if mode in (ANGLE_DEG, ANGLE_RAD, ANGLE_GRAD):
            self.angle_mode = mode

    # --- Angle Conversion Helpers ---
    def _to_radians(self, val: float) -> float:
        if self.angle_mode == ANGLE_DEG:
            return math.radians(val)
        elif self.angle_mode == ANGLE_GRAD:
            return val * (math.pi / 200.0)
        return val

    def _from_radians(self, val: float) -> float:
        if self.angle_mode == ANGLE_DEG:
            return math.degrees(val)
        elif self.angle_mode == ANGLE_GRAD:
            return val * (200.0 / math.pi)
        return val

    # --- Trigonometric Functions (Respecting Angle Mode) ---
    def _sin(self, x: float) -> float:
        # Clean small artifacts like sin(180°) = 1.22e-16 -> 0
        rad = self._to_radians(x)
        res = math.sin(rad)
        return 0.0 if abs(res) < 1e-15 else res

    def _cos(self, x: float) -> float:
        rad = self._to_radians(x)
        res = math.cos(rad)
        return 0.0 if abs(res) < 1e-15 else res

    def _tan(self, x: float) -> float:
        rad = self._to_radians(x)
        # Check for asymptote (cos(rad) ~ 0)
        c = math.cos(rad)
        if abs(c) < 1e-15:
            raise ValueError("Tangent undefined (asymptote)")
        res = math.tan(rad)
        return 0.0 if abs(res) < 1e-15 else res

    def _cot(self, x: float) -> float:
        t = self._tan(x)
        if abs(t) < 1e-15:
            raise ZeroDivisionError("Cotangent undefined (division by zero)")
        return 1.0 / t

    def _sec(self, x: float) -> float:
        c = self._cos(x)
        if abs(c) < 1e-15:
            raise ZeroDivisionError("Secant undefined (division by zero)")
        return 1.0 / c

    def _csc(self, x: float) -> float:
        s = self._sin(x)
        if abs(s) < 1e-15:
            raise ZeroDivisionError("Cosecant undefined (division by zero)")
        return 1.0 / s

    def _asin(self, x: float) -> float:
        if x < -1.0 or x > 1.0:
            raise ValueError("asin domain error: input must be between -1 and 1")
        return self._from_radians(math.asin(x))

    def _acos(self, x: float) -> float:
        if x < -1.0 or x > 1.0:
            raise ValueError("acos domain error: input must be between -1 and 1")
        return self._from_radians(math.acos(x))

    def _atan(self, x: float) -> float:
        return self._from_radians(math.atan(x))

    # --- Hyperbolic Functions ---
    def _sinh(self, x: float) -> float:
        return math.sinh(x)

    def _cosh(self, x: float) -> float:
        return math.cosh(x)

    def _tanh(self, x: float) -> float:
        return math.tanh(x)

    def _asinh(self, x: float) -> float:
        return math.asinh(x)

    def _acosh(self, x: float) -> float:
        if x < 1.0:
            raise ValueError("acosh domain error: input must be >= 1")
        return math.acosh(x)

    def _atanh(self, x: float) -> float:
        if x <= -1.0 or x >= 1.0:
            raise ValueError("atanh domain error: input must be between -1 and 1")
        return math.atanh(x)

    # --- Combinatorics & Advanced Math ---
    def _factorial(self, n: float) -> int:
        if not float(n).is_integer() or n < 0:
            raise ValueError("Factorial is only defined for non-negative integers")
        int_n = int(n)
        if int_n > 500:
            raise OverflowError("Factorial value too large to compute safely")
        return math.factorial(int_n)

    def _nPr(self, n: float, r: float) -> int:
        if not float(n).is_integer() or not float(r).is_integer():
            raise ValueError("Permutation (nPr) requires integer arguments")
        int_n, int_r = int(n), int(r)
        if int_n < 0 or int_r < 0 or int_r > int_n:
            raise ValueError("Invalid n or r for permutation: requires n >= r >= 0")
        return math.perm(int_n, int_r)

    def _nCr(self, n: float, r: float) -> int:
        if not float(n).is_integer() or not float(r).is_integer():
            raise ValueError("Combination (nCr) requires integer arguments")
        int_n, int_r = int(n), int(r)
        if int_n < 0 or int_r < 0 or int_r > int_n:
            raise ValueError("Invalid n or r for combination: requires n >= r >= 0")
        return math.comb(int_n, int_r)

    def _cbrt(self, x: float) -> float:
        if x >= 0:
            return math.pow(x, 1.0 / 3.0)
        else:
            return -math.pow(-x, 1.0 / 3.0)

    def _log_base(self, x: float, base: float = 10.0) -> float:
        if x <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers")
        if base <= 0 or base == 1:
            raise ValueError("Logarithm base must be positive and not equal to 1")
        return math.log(x, base)

    def _ln(self, x: float) -> float:
        if x <= 0:
            raise ValueError("Natural logarithm undefined for non-positive numbers")
        return math.log(x)

    def _sign(self, x: float) -> int:
        if x > 0:
            return 1
        elif x < 0:
            return -1
        return 0

    def _get_function_map(self):
        return {
            "sin": self._sin,
            "cos": self._cos,
            "tan": self._tan,
            "cot": self._cot,
            "sec": self._sec,
            "csc": self._csc,
            "asin": self._asin,
            "acos": self._acos,
            "atan": self._atan,
            "sinh": self._sinh,
            "cosh": self._cosh,
            "tanh": self._tanh,
            "asinh": self._asinh,
            "acosh": self._acosh,
            "atanh": self._atanh,
            "sqrt": math.sqrt,
            "cbrt": self._cbrt,
            "log": self._log_base,
            "log10": math.log10,
            "log2": math.log2,
            "ln": self._ln,
            "exp": math.exp,
            "abs": abs,
            "floor": math.floor,
            "ceil": math.ceil,
            "round": round,
            "sign": self._sign,
            "factorial": self._factorial,
            "fact": self._factorial,
            "nPr": self._nPr,
            "nCr": self._nCr,
        }

    def _get_constant_map(self):
        return {
            "pi": PI,
            "e": E,
            "phi": PHI,
        }

    # --- Preprocessing ---
    def preprocess_expression(self, expr: str) -> str:
        """Sanitize and normalize raw user expression into a parseable Python AST math string."""
        s = expr.strip()
        if not s:
            return ""

        # Normalize unicode math symbols
        s = s.replace("×", "*").replace("÷", "/")
        s = s.replace("−", "-").replace("—", "-")
        s = s.replace("^", "**")
        s = s.replace("π", "pi")
        s = s.replace("φ", "phi")

        # Convert √144 or √(144) to sqrt(144)
        s = re.sub(r"√\s*(\d+(?:\.\d+)?|\([^\)]+\))", r"sqrt(\1)", s)
        s = s.replace("√", "sqrt")

        # Convert nPr syntax: e.g., 10P3 or 10 p 3 -> nPr(10, 3)
        s = re.sub(r"(\d+)\s*[Pp]\s*(\d+)", r"nPr(\1, \2)", s)

        # Convert nCr syntax: e.g., 10C3 or 10 c 3 -> nCr(10, 3)
        s = re.sub(r"(\d+)\s*[Cc]\s*(\d+)", r"nCr(\1, \2)", s)

        # Convert factorial postfix: e.g. 5! -> factorial(5), (2+3)! -> factorial(2+3)
        # Handle chained factorials like 5!! -> factorial(factorial(5))
        while "!" in s:
            new_s = re.sub(r"(\((?:[^)(]+|\([^)(]*\))*\)|\d+(?:\.\d+)?)\s*!", r"factorial(\1)", s)
            if new_s == s:
                break
            s = new_s

        # Percentage calculations in expressions:
        # e.g. 200 + 10% -> 200 + (200 * 10 / 100)
        # e.g. 200 * 10% -> 200 * (10 / 100)
        # First handle standard single number percentage: number%
        s = re.sub(r"(\d+(?:\.\d+)?)\s*%", r"(\1 / 100)", s)

        # Implicit multiplication:
        # 1. Number (not part of an identifier) followed by parenthesis: 2(3) -> 2*(3)
        s = re.sub(r"(?<![a-zA-Z0-9_.])(\d+(?:\.\d+)?)\s*\(", r"\1*(", s)
        # 2. Closing parenthesis followed by opening: )( -> )*(
        s = re.sub(r"\)\s*\(", r")*(", s)
        # 3. Closing parenthesis followed by number: )2 -> )*2
        s = re.sub(r"\)\s*(\d+(?:\.\d+)?)", r")*\1", s)
        # 4. Number followed by constant or function: 2pi -> 2*pi, 3sin(x) -> 3*sin(x)
        s = re.sub(r"(?<![a-zA-Z0-9_.])(\d+(?:\.\d+)?)\s*([a-zA-Z_]\w*)", r"\1*\2", s)

        return s

    # --- Safe AST Evaluation ---
    def _eval_node(self, node: ast.AST) -> Any:
        func_map = self._get_function_map()
        const_map = self._get_constant_map()

        if isinstance(node, ast.Expression):
            return self._eval_node(node.body)

        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value)}")

        elif isinstance(node, ast.Name):
            name_lower = node.id.lower()
            if name_lower in const_map:
                return const_map[name_lower]
            raise ValueError(f"Unknown variable or constant: '{node.id}'")

        elif isinstance(node, ast.UnaryOp):
            val = self._eval_node(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +val
            elif isinstance(node.op, ast.USub):
                return -val
            raise ValueError(f"Unsupported unary operator: {type(node.op)}")

        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)

            if isinstance(node.op, ast.Add):
                return left + right
            elif isinstance(node.op, ast.Sub):
                return left - right
            elif isinstance(node.op, ast.Mult):
                return left * right
            elif isinstance(node.op, ast.Div):
                if right == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                return left / right
            elif isinstance(node.op, ast.FloorDiv):
                if right == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                return left // right
            elif isinstance(node.op, ast.Mod):
                if right == 0:
                    raise ZeroDivisionError("Cannot divide by zero (modulo)")
                return left % right
            elif isinstance(node.op, ast.Pow):
                # Guard against dangerous huge powers that freeze execution
                if abs(left) > 1 and right > 10000:
                    raise OverflowError("Exponent too large to evaluate")
                try:
                    res = left ** right
                    if isinstance(res, complex):
                        raise ValueError("Real numbers only: result is complex")
                    return res
                except OverflowError:
                    raise OverflowError("Number too large (Overflow)")

            raise ValueError(f"Unsupported binary operator: {type(node.op)}")

        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Nested function attribute calls are forbidden")

            func_name = node.func.id
            if func_name not in func_map:
                raise ValueError(f"Unknown or unsupported function: '{func_name}'")

            args = [self._eval_node(arg) for arg in node.args]
            fn = func_map[func_name]

            try:
                return fn(*args)
            except TypeError as te:
                raise ValueError(f"Incorrect arguments for function '{func_name}': {te}")

        else:
            raise ValueError(f"Forbidden or unsupported expression syntax: {type(node).__name__}")

    def evaluate(self, expr: str) -> Tuple[bool, Union[float, int, str]]:
        """Evaluate a mathematical expression string safely.
        
        Returns:
            Tuple[bool, result]:
                - (True, numeric_result) on success
                - (False, error_message_string) on failure
        """
        if not expr or not expr.strip():
            return False, "Empty expression"

        try:
            # Check balanced parentheses
            if expr.count("(") != expr.count(")"):
                return False, "Unmatched parentheses"

            processed = self.preprocess_expression(expr)
            if not processed:
                return False, "Empty expression"

            tree = ast.parse(processed, mode="eval")
            result = self._eval_node(tree)

            # Round microscopic floating error
            if isinstance(result, float):
                if math.isnan(result):
                    return False, "Result is undefined (NaN)"
                if math.isinf(result):
                    return False, "Result is infinite (Infinity)"
                rounded = round(result, 12)
                if rounded.is_integer():
                    result = int(rounded)
                else:
                    result = rounded

            return True, result

        except ZeroDivisionError as zde:
            return False, str(zde)
        except OverflowError as oe:
            return False, str(oe)
        except ValueError as ve:
            return False, str(ve)
        except SyntaxError:
            return False, "Invalid expression syntax"
        except Exception as e:
            return False, f"Evaluation error: {str(e)}"
