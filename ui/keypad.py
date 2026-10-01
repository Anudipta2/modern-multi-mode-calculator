"""Calculator keypad components for Standard and Scientific modes."""

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor


class StandardKeypad(QWidget):
    """Standard everyday arithmetic keypad with touch-friendly dimensions."""

    digit_pressed = Signal(str)
    operator_pressed = Signal(str)
    equals_pressed = Signal()
    clear_all_pressed = Signal()
    backspace_pressed = Signal()
    decimal_pressed = Signal()
    toggle_sign_pressed = Signal()
    percentage_pressed = Signal()
    parenthesis_pressed = Signal(str)
    memory_pressed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)

        # --- Memory Bar ---
        mem_layout = QHBoxLayout()
        mem_layout.setSpacing(8)
        mem_buttons = ["MC", "MR", "M+", "M-", "MS"]
        for label in mem_buttons:
            btn = QPushButton(label)
            btn.setProperty("class", "btn-memory")
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.clicked.connect(lambda _, l=label: self.memory_pressed.emit(l))
            mem_layout.addWidget(btn)
        main_layout.addLayout(mem_layout)

        # --- Standard Grid Keypad ---
        grid = QGridLayout()
        grid.setSpacing(10)

        # Layout plan:
        # Row 0: AC,  ±,   %,   ÷
        # Row 1: 7,   8,   9,   ×
        # Row 2: 4,   5,   6,   −
        # Row 3: 1,   2,   3,   +
        # Row 4: 0,   .,   ⌫,   =

        buttons_def = [
            ("AC", 0, 0, "btn-util", self.clear_all_pressed.emit),
            ("±", 0, 1, "btn-util", self.toggle_sign_pressed.emit),
            ("%", 0, 2, "btn-util", self.percentage_pressed.emit),
            ("÷", 0, 3, "btn-operator", lambda: self.operator_pressed.emit("÷")),

            ("7", 1, 0, "btn-number", lambda: self.digit_pressed.emit("7")),
            ("8", 1, 1, "btn-number", lambda: self.digit_pressed.emit("8")),
            ("9", 1, 2, "btn-number", lambda: self.digit_pressed.emit("9")),
            ("×", 1, 3, "btn-operator", lambda: self.operator_pressed.emit("×")),

            ("4", 2, 0, "btn-number", lambda: self.digit_pressed.emit("4")),
            ("5", 2, 1, "btn-number", lambda: self.digit_pressed.emit("5")),
            ("6", 2, 2, "btn-number", lambda: self.digit_pressed.emit("6")),
            ("−", 2, 3, "btn-operator", lambda: self.operator_pressed.emit("−")),

            ("1", 3, 0, "btn-number", lambda: self.digit_pressed.emit("1")),
            ("2", 3, 1, "btn-number", lambda: self.digit_pressed.emit("2")),
            ("3", 3, 2, "btn-number", lambda: self.digit_pressed.emit("3")),
            ("+", 3, 3, "btn-operator", lambda: self.operator_pressed.emit("+")),

            ("0", 4, 0, "btn-number", lambda: self.digit_pressed.emit("0")),
            (".", 4, 1, "btn-number", self.decimal_pressed.emit),
            ("⌫", 4, 2, "btn-util", self.backspace_pressed.emit),
            ("=", 4, 3, "btn-equals", self.equals_pressed.emit),
        ]

        for text, r, c, cls_name, slot in buttons_def:
            btn = QPushButton(text)
            btn.setProperty("class", f"calc-btn {cls_name}")
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.clicked.connect(slot)
            grid.addWidget(btn, r, c)

        main_layout.addLayout(grid)


class ScientificKeypad(QWidget):
    """Scientific Keypad integrating scientific functions, constants, and standard numbers."""

    digit_pressed = Signal(str)
    operator_pressed = Signal(str)
    unary_func_pressed = Signal(str)
    constant_pressed = Signal(str)
    parenthesis_pressed = Signal(str)
    equals_pressed = Signal()
    clear_all_pressed = Signal()
    backspace_pressed = Signal()
    decimal_pressed = Signal()
    toggle_sign_pressed = Signal()
    percentage_pressed = Signal()
    memory_pressed = Signal(str)
    angle_mode_toggle_pressed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_second = False
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        # --- Memory Bar ---
        mem_layout = QHBoxLayout()
        mem_layout.setSpacing(6)
        mem_buttons = ["MC", "MR", "M+", "M-", "MS"]
        for label in mem_buttons:
            btn = QPushButton(label)
            btn.setProperty("class", "btn-memory")
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.clicked.connect(lambda _, l=label: self.memory_pressed.emit(l))
            mem_layout.addWidget(btn)
        main_layout.addLayout(mem_layout)

        # Combined Grid: 6 columns, 6 rows
        # Col 0-2: Scientific functions
        # Col 3-5: Standard numbers and operators
        grid = QGridLayout()
        grid.setSpacing(8)

        # Row 0: 2nd, DEG/RAD, sin,      AC,  ⌫,   ÷
        # Row 1: cos, tan,     cot,      7,   8,   9,   ×
        # Row 2: ln,  log10,   sqrt,     4,   5,   6,   −
        # Row 3: x^2, x^y,     1/x,      1,   2,   3,   +
        # Row 4: n!,  nPr,     nCr,      0,   .,   %
        # Row 5: (,   ),       pi,       e,   ±,   =

        self.btn_2nd = QPushButton("2nd")
        self.btn_2nd.setProperty("class", "calc-btn btn-scientific")
        self.btn_2nd.setCheckable(True)
        self.btn_2nd.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_2nd.clicked.connect(self._toggle_second)

        self.btn_sin = QPushButton("sin")
        self.btn_cos = QPushButton("cos")
        self.btn_tan = QPushButton("tan")
        self.btn_cot = QPushButton("cot")
        self.btn_sec = QPushButton("sec")
        self.btn_csc = QPushButton("csc")

        self.btn_ln = QPushButton("ln")
        self.btn_log = QPushButton("log₁₀")
        self.btn_sqrt = QPushButton("√x")
        self.btn_cbrt = QPushButton("∛x")
        self.btn_sqr = QPushButton("x²")
        self.btn_pow = QPushButton("xʸ")
        self.btn_recip = QPushButton("1/x")
        self.btn_fact = QPushButton("n!")
        self.btn_npr = QPushButton("nPr")
        self.btn_ncr = QPushButton("nCr")

        # Scientific keys config
        sci_buttons = [
            (self.btn_2nd, 0, 0, None),
            (QPushButton("("), 0, 1, lambda: self.parenthesis_pressed.emit("(")),
            (QPushButton(")"), 0, 2, lambda: self.parenthesis_pressed.emit(")")),

            (self.btn_sin, 1, 0, lambda: self._on_trig("sin")),
            (self.btn_cos, 1, 1, lambda: self._on_trig("cos")),
            (self.btn_tan, 1, 2, lambda: self._on_trig("tan")),

            (self.btn_ln, 2, 0, lambda: self._on_log("ln")),
            (self.btn_log, 2, 1, lambda: self._on_log("log10")),
            (self.btn_sqrt, 2, 2, lambda: self._on_root("sqrt")),

            (self.btn_sqr, 3, 0, lambda: self._on_power("x^2")),
            (self.btn_pow, 3, 1, lambda: self.operator_pressed.emit("^")),
            (self.btn_recip, 3, 2, lambda: self.unary_func_pressed.emit("1/x")),

            (self.btn_fact, 4, 0, lambda: self.unary_func_pressed.emit("factorial")),
            (self.btn_npr, 4, 1, lambda: self.operator_pressed.emit("nPr")),
            (self.btn_ncr, 4, 2, lambda: self.operator_pressed.emit("nCr")),

            (QPushButton("π"), 5, 0, lambda: self.constant_pressed.emit("pi")),
            (QPushButton("e"), 5, 1, lambda: self.constant_pressed.emit("e")),
            (QPushButton("φ"), 5, 2, lambda: self.constant_pressed.emit("phi")),
        ]

        for btn, r, c, slot in sci_buttons:
            btn.setProperty("class", "calc-btn btn-scientific")
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            if slot:
                btn.clicked.connect(slot)
            grid.addWidget(btn, r, c)

        # Standard keys alongside
        numpad_buttons = [
            ("AC", 0, 3, "btn-util", self.clear_all_pressed.emit),
            ("⌫", 0, 4, "btn-util", self.backspace_pressed.emit),
            ("÷", 0, 5, "btn-operator", lambda: self.operator_pressed.emit("÷")),

            ("7", 1, 3, "btn-number", lambda: self.digit_pressed.emit("7")),
            ("8", 1, 4, "btn-number", lambda: self.digit_pressed.emit("8")),
            ("9", 1, 5, "btn-number", lambda: self.digit_pressed.emit("9")),
            ("×", 1, 5, "btn-operator", lambda: self.operator_pressed.emit("×")),

            ("4", 2, 3, "btn-number", lambda: self.digit_pressed.emit("4")),
            ("5", 2, 4, "btn-number", lambda: self.digit_pressed.emit("5")),
            ("6", 2, 5, "btn-number", lambda: self.digit_pressed.emit("6")),
            ("−", 2, 6, "btn-operator", lambda: self.operator_pressed.emit("−")),

            ("1", 3, 3, "btn-number", lambda: self.digit_pressed.emit("1")),
            ("2", 3, 4, "btn-number", lambda: self.digit_pressed.emit("2")),
            ("3", 3, 5, "btn-number", lambda: self.digit_pressed.emit("3")),
            ("+", 3, 6, "btn-operator", lambda: self.operator_pressed.emit("+")),

            ("0", 4, 3, "btn-number", lambda: self.digit_pressed.emit("0")),
            (".", 4, 4, "btn-number", self.decimal_pressed.emit),
            ("%", 4, 5, "btn-util", self.percentage_pressed.emit),
            ("±", 4, 6, "btn-util", self.toggle_sign_pressed.emit),

            ("=", 5, 3, "btn-equals", self.equals_pressed.emit),
        ]

        # Let's cleanly layout the standard block in columns 3, 4, 5, 6
        # Col 3: 7, 4, 1, 0
        # Col 4: 8, 5, 2, .
        # Col 5: 9, 6, 3, %
        # Col 6: ÷, ×, −, +, =
        grid.addWidget(self._make_btn("AC", "btn-util", self.clear_all_pressed.emit), 0, 3)
        grid.addWidget(self._make_btn("⌫", "btn-util", self.backspace_pressed.emit), 0, 4)
        grid.addWidget(self._make_btn("±", "btn-util", self.toggle_sign_pressed.emit), 0, 5)
        grid.addWidget(self._make_btn("÷", "btn-operator", lambda: self.operator_pressed.emit("÷")), 0, 6)

        grid.addWidget(self._make_btn("7", "btn-number", lambda: self.digit_pressed.emit("7")), 1, 3)
        grid.addWidget(self._make_btn("8", "btn-number", lambda: self.digit_pressed.emit("8")), 1, 4)
        grid.addWidget(self._make_btn("9", "btn-number", lambda: self.digit_pressed.emit("9")), 1, 5)
        grid.addWidget(self._make_btn("×", "btn-operator", lambda: self.operator_pressed.emit("×")), 1, 6)

        grid.addWidget(self._make_btn("4", "btn-number", lambda: self.digit_pressed.emit("4")), 2, 3)
        grid.addWidget(self._make_btn("5", "btn-number", lambda: self.digit_pressed.emit("5")), 2, 4)
        grid.addWidget(self._make_btn("6", "btn-number", lambda: self.digit_pressed.emit("6")), 2, 5)
        grid.addWidget(self._make_btn("−", "btn-operator", lambda: self.operator_pressed.emit("−")), 2, 6)

        grid.addWidget(self._make_btn("1", "btn-number", lambda: self.digit_pressed.emit("1")), 3, 3)
        grid.addWidget(self._make_btn("2", "btn-number", lambda: self.digit_pressed.emit("2")), 3, 4)
        grid.addWidget(self._make_btn("3", "btn-number", lambda: self.digit_pressed.emit("3")), 3, 5)
        grid.addWidget(self._make_btn("+", "btn-operator", lambda: self.operator_pressed.emit("+")), 3, 6)

        grid.addWidget(self._make_btn("0", "btn-number", lambda: self.digit_pressed.emit("0")), 4, 3)
        grid.addWidget(self._make_btn(".", "btn-number", self.decimal_pressed.emit), 4, 4)
        grid.addWidget(self._make_btn("%", "btn-util", self.percentage_pressed.emit), 4, 5)
        grid.addWidget(self._make_btn("Rand", "btn-util", lambda: self.unary_func_pressed.emit("rand")), 4, 6)

        # Equals spans columns 3 to 6 on bottom row
        equals_btn = self._make_btn("=", "btn-equals", self.equals_pressed.emit)
        grid.addWidget(equals_btn, 5, 3, 1, 4)

        main_layout.addLayout(grid)

    def _make_btn(self, text, cls_name, slot):
        btn = QPushButton(text)
        btn.setProperty("class", f"calc-btn {cls_name}")
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btn.clicked.connect(slot)
        return btn

    def _toggle_second(self):
        self.is_second = self.btn_2nd.isChecked()
        if self.is_second:
            self.btn_sin.setText("sin⁻¹")
            self.btn_cos.setText("cos⁻¹")
            self.btn_tan.setText("tan⁻¹")
            self.btn_ln.setText("eˣ")
            self.btn_log.setText("10ˣ")
            self.btn_sqrt.setText("∛x")
            self.btn_sqr.setText("x³")
        else:
            self.btn_sin.setText("sin")
            self.btn_cos.setText("cos")
            self.btn_tan.setText("tan")
            self.btn_ln.setText("ln")
            self.btn_log.setText("log₁₀")
            self.btn_sqrt.setText("√x")
            self.btn_sqr.setText("x²")

    def _on_trig(self, func: str):
        if self.is_second:
            inv_map = {"sin": "asin", "cos": "acos", "tan": "atan"}
            self.unary_func_pressed.emit(inv_map.get(func, func))
        else:
            self.unary_func_pressed.emit(func)

    def _on_log(self, func: str):
        if self.is_second:
            alt_map = {"ln": "e^x", "log10": "10^x"}
            self.unary_func_pressed.emit(alt_map.get(func, func))
        else:
            self.unary_func_pressed.emit(func)

    def _on_root(self, func: str):
        if self.is_second:
            self.unary_func_pressed.emit("cbrt")
        else:
            self.unary_func_pressed.emit("sqrt")

    def _on_power(self, func: str):
        if self.is_second:
            self.unary_func_pressed.emit("x^3")
        else:
            self.unary_func_pressed.emit("x^2")
