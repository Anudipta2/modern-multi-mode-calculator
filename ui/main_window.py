"""Master MainWindow integrating Display, Keypads, Business View, and History Drawer."""

import os
import sys

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QApplication,
    QSplitter,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QKeyEvent, QKeySequence, QIcon

from core.constants import MODE_STANDARD, MODE_SCIENTIFIC, MODE_BUSINESS
from core.history import HistoryManager
from calculators.standard import StandardCalculatorEngine
from calculators.scientific import ScientificCalculatorEngine
from calculators.business import BusinessCalculatorEngine

from ui.styles import GLASS_THEME_QSS
from ui.mode_selector import ModeSelector
from ui.calculator_display import CalculatorDisplay
from ui.keypad import StandardKeypad, ScientificKeypad
from ui.business_view import BusinessView
from ui.history_panel import HistoryPanel


class ModernCalculatorWindow(QMainWindow):
    """Main Application Window for the Modern Apple-Inspired Multi-Mode Calculator."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Multi-Mode Calculator")
        self.setMinimumSize(450, 680)
        self.resize(520, 750)

        # Initialize Data & Calculation Engines
        self.history_manager = HistoryManager()
        self.standard_engine = StandardCalculatorEngine()
        self.scientific_engine = ScientificCalculatorEngine()
        self.business_engine = BusinessCalculatorEngine()

        self.current_mode = MODE_STANDARD

        # Set Window Icon
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(base_dir, "assets", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Apply Global Dark Glass Theme
        self.setStyleSheet(GLASS_THEME_QSS)

        self._init_ui()
        self._wire_signals()
        self._update_display_from_active_engine()

    def _init_ui(self):
        # Central container
        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(14, 14, 14, 14)
        root_layout.setSpacing(12)

        # Left / Main Calculator Column
        self.main_calc_widget = QWidget()
        calc_layout = QVBoxLayout(self.main_calc_widget)
        calc_layout.setContentsMargins(0, 0, 0, 0)
        calc_layout.setSpacing(12)

        # 1. Top Bar Mode Selector
        self.mode_selector = ModeSelector()
        calc_layout.addWidget(self.mode_selector)

        # 2. Glass Display Card
        self.display_card = CalculatorDisplay()
        calc_layout.addWidget(self.display_card)

        # 3. Stacked Keypads / Views
        self.stack = QStackedWidget()

        self.standard_keypad = StandardKeypad()
        self.scientific_keypad = ScientificKeypad()
        self.business_view = BusinessView(self.business_engine)

        self.stack.addWidget(self.standard_keypad)    # Index 0
        self.stack.addWidget(self.scientific_keypad)  # Index 1
        self.stack.addWidget(self.business_view)      # Index 2

        calc_layout.addWidget(self.stack, 1)

        root_layout.addWidget(self.main_calc_widget, 1)

        # 4. Collapsible History Drawer on the Right
        self.history_panel = HistoryPanel(self.history_manager)
        self.history_panel.hide()
        root_layout.addWidget(self.history_panel)

    def _wire_signals(self):
        # Mode selector signals
        self.mode_selector.mode_changed.connect(self.set_mode)
        self.mode_selector.history_toggled.connect(self._toggle_history)

        # History panel signals
        self.history_panel.close_requested.connect(self._toggle_history)
        self.history_panel.entry_selected.connect(self._on_history_entry_reused)

        # Display signals
        self.display_card.angle_mode_toggled.connect(self._on_angle_mode_toggled)

        # Business view signals
        self.business_view.calculation_completed.connect(self._on_business_calc_completed)

        # --- Standard Keypad Wiring ---
        self.standard_keypad.digit_pressed.connect(self._on_standard_digit)
        self.standard_keypad.operator_pressed.connect(self._on_standard_operator)
        self.standard_keypad.equals_pressed.connect(self._on_standard_equals)
        self.standard_keypad.clear_all_pressed.connect(self._on_standard_clear_all)
        self.standard_keypad.backspace_pressed.connect(self._on_standard_backspace)
        self.standard_keypad.decimal_pressed.connect(self._on_standard_decimal)
        self.standard_keypad.toggle_sign_pressed.connect(self._on_standard_toggle_sign)
        self.standard_keypad.percentage_pressed.connect(self._on_standard_percentage)
        self.standard_keypad.parenthesis_pressed.connect(self._on_standard_parenthesis)
        self.standard_keypad.memory_pressed.connect(self._on_standard_memory)

        # --- Scientific Keypad Wiring ---
        self.scientific_keypad.digit_pressed.connect(self._on_scientific_digit)
        self.scientific_keypad.operator_pressed.connect(self._on_scientific_operator)
        self.scientific_keypad.unary_func_pressed.connect(self._on_scientific_unary)
        self.scientific_keypad.constant_pressed.connect(self._on_scientific_constant)
        self.scientific_keypad.parenthesis_pressed.connect(self._on_scientific_parenthesis)
        self.scientific_keypad.equals_pressed.connect(self._on_scientific_equals)
        self.scientific_keypad.clear_all_pressed.connect(self._on_scientific_clear_all)
        self.scientific_keypad.backspace_pressed.connect(self._on_scientific_backspace)
        self.scientific_keypad.decimal_pressed.connect(self._on_scientific_decimal)
        self.scientific_keypad.toggle_sign_pressed.connect(self._on_scientific_toggle_sign)
        self.scientific_keypad.percentage_pressed.connect(self._on_scientific_percentage)
        self.scientific_keypad.memory_pressed.connect(self._on_scientific_memory)

    # --- Mode Switching ---
    def set_mode(self, mode: str):
        if mode == self.current_mode:
            return

        prev_mode = self.current_mode
        self.current_mode = mode

        # Transfer current value between standard and scientific smoothly
        if prev_mode == MODE_STANDARD and mode == MODE_SCIENTIFIC:
            val = self.standard_engine.get_raw_display()
            self.scientific_engine.display_value = val
            self.scientific_engine.is_new_entry = self.standard_engine.is_new_entry
        elif prev_mode == MODE_SCIENTIFIC and mode == MODE_STANDARD:
            val = self.scientific_engine.get_raw_display()
            self.standard_engine.display_value = val
            self.standard_engine.is_new_entry = self.scientific_engine.is_new_entry

        if mode == MODE_STANDARD:
            self.stack.setCurrentIndex(0)
            self.display_card.show()
            self.display_card.set_mode_badge("STANDARD", show_angle=False)
            self._update_display_from_active_engine()
            self.resize_for_mode(520, 750)

        elif mode == MODE_SCIENTIFIC:
            self.stack.setCurrentIndex(1)
            self.display_card.show()
            self.display_card.set_mode_badge(
                "SCIENTIFIC",
                show_angle=True,
                angle_mode=self.scientific_engine.angle_mode,
            )
            self._update_display_from_active_engine()
            self.resize_for_mode(720, 780)

        elif mode == MODE_BUSINESS:
            self.stack.setCurrentIndex(2)
            self.display_card.hide()  # Business view has dedicated custom result cards
            self.resize_for_mode(680, 780)

    def resize_for_mode(self, target_width: int, target_height: int):
        if self.history_panel.isVisible():
            target_width += 330
        if self.width() < target_width:
            self.resize(target_width, max(self.height(), target_height))

    def _toggle_history(self):
        is_visible = not self.history_panel.isVisible()
        self.history_panel.setVisible(is_visible)
        self.mode_selector.set_history_active(is_visible)
        if is_visible:
            self.history_panel.refresh()
            self.resize(self.width() + 330, self.height())
        else:
            self.resize(max(450, self.width() - 330), self.height())

    def _on_angle_mode_toggled(self):
        new_mode = self.scientific_engine.toggle_angle_mode()
        self.display_card.set_mode_badge("SCIENTIFIC", show_angle=True, angle_mode=new_mode)

    # --- Standard Calculator Handlers ---
    def _on_standard_digit(self, digit: str):
        self.standard_engine.input_digit(digit)
        self._update_display_from_active_engine()

    def _on_standard_operator(self, op: str):
        self.standard_engine.input_operator(op)
        self._update_display_from_active_engine()

    def _on_standard_equals(self):
        expr_before = self.standard_engine.get_expression()
        val_before = self.standard_engine.get_raw_display()
        ok, res = self.standard_engine.calculate()
        self._update_display_from_active_engine()
        if ok and expr_before:
            full_expr = f"{expr_before} {val_before}" if not expr_before.endswith("=") else expr_before
            self.history_manager.add_entry(full_expr, res, mode=MODE_STANDARD)
            if self.history_panel.isVisible():
                self.history_panel.refresh()

    def _on_standard_clear_all(self):
        self.standard_engine.clear_all()
        self._update_display_from_active_engine()

    def _on_standard_backspace(self):
        self.standard_engine.backspace()
        self._update_display_from_active_engine()

    def _on_standard_decimal(self):
        self.standard_engine.input_decimal()
        self._update_display_from_active_engine()

    def _on_standard_toggle_sign(self):
        self.standard_engine.toggle_sign()
        self._update_display_from_active_engine()

    def _on_standard_percentage(self):
        self.standard_engine.percentage()
        self._update_display_from_active_engine()

    def _on_standard_parenthesis(self, p: str):
        self.standard_engine.input_parenthesis(p)
        self._update_display_from_active_engine()

    def _on_standard_memory(self, action: str):
        if action == "MC":
            self.standard_engine.memory_clear()
        elif action == "MR":
            self.standard_engine.memory_recall()
        elif action == "M+":
            self.standard_engine.memory_add()
        elif action == "M-":
            self.standard_engine.memory_subtract()
        elif action == "MS":
            self.standard_engine.memory_store()
        self._update_display_from_active_engine()

    # --- Scientific Calculator Handlers ---
    def _on_scientific_digit(self, digit: str):
        self.scientific_engine.input_digit(digit)
        self._update_display_from_active_engine()

    def _on_scientific_operator(self, op: str):
        self.scientific_engine.input_operator(op)
        self._update_display_from_active_engine()

    def _on_scientific_unary(self, func: str):
        val_before = self.scientific_engine.get_raw_display()
        self.scientific_engine.apply_unary_function(func)
        self._update_display_from_active_engine()
        res = self.scientific_engine.get_raw_display()
        if not self.scientific_engine.has_error:
            self.history_manager.add_entry(f"{func}({val_before})", res, mode=MODE_SCIENTIFIC)
            if self.history_panel.isVisible():
                self.history_panel.refresh()

    def _on_scientific_constant(self, const_name: str):
        self.scientific_engine.input_constant(const_name)
        self._update_display_from_active_engine()

    def _on_scientific_parenthesis(self, p: str):
        self.scientific_engine.input_parenthesis(p)
        self._update_display_from_active_engine()

    def _on_scientific_equals(self):
        expr_before = self.scientific_engine.get_expression()
        val_before = self.scientific_engine.get_raw_display()
        ok, res = self.scientific_engine.calculate()
        self._update_display_from_active_engine()
        if ok and expr_before:
            full_expr = f"{expr_before} {val_before}" if not expr_before.endswith("=") else expr_before
            self.history_manager.add_entry(full_expr, res, mode=MODE_SCIENTIFIC)
            if self.history_panel.isVisible():
                self.history_panel.refresh()

    def _on_scientific_clear_all(self):
        self.scientific_engine.clear_all()
        self._update_display_from_active_engine()

    def _on_scientific_backspace(self):
        self.scientific_engine.backspace()
        self._update_display_from_active_engine()

    def _on_scientific_decimal(self):
        self.scientific_engine.input_decimal()
        self._update_display_from_active_engine()

    def _on_scientific_toggle_sign(self):
        self.scientific_engine.toggle_sign()
        self._update_display_from_active_engine()

    def _on_scientific_percentage(self):
        self.scientific_engine.input_operator("%")
        self._update_display_from_active_engine()

    def _on_scientific_memory(self, action: str):
        if action == "MC":
            self.scientific_engine.memory_clear()
        elif action == "MR":
            self.scientific_engine.memory_recall()
        elif action == "M+":
            self.scientific_engine.memory_add()
        elif action == "M-":
            self.scientific_engine.memory_subtract()
        elif action == "MS":
            self.scientific_engine.memory_store()
        self._update_display_from_active_engine()

    # --- Business View Handlers ---
    def _on_business_calc_completed(self, expr: str, res: str):
        self.history_manager.add_entry(expr, res, mode=MODE_BUSINESS)
        if self.history_panel.isVisible():
            self.history_panel.refresh()

    def _on_history_entry_reused(self, result_text: str):
        # Clean currency symbols, commas or equals signs
        clean_num = result_text.replace("₹", "").replace("$", "").replace("€", "").replace("£", "").replace("¥", "").replace(",", "").replace("=", "").strip()
        if self.current_mode == MODE_STANDARD:
            self.standard_engine.display_value = clean_num
            self.standard_engine.is_new_entry = True
            self._update_display_from_active_engine()
        elif self.current_mode == MODE_SCIENTIFIC:
            self.scientific_engine.display_value = clean_num
            self.scientific_engine.is_new_entry = True
            self._update_display_from_active_engine()

    def _update_display_from_active_engine(self):
        if self.current_mode == MODE_STANDARD:
            self.display_card.set_expression(self.standard_engine.get_expression())
            self.display_card.set_result(self.standard_engine.get_display())
            self.display_card.set_memory_active(self.standard_engine.has_memory)
        elif self.current_mode == MODE_SCIENTIFIC:
            self.display_card.set_expression(self.scientific_engine.get_expression())
            self.display_card.set_result(self.scientific_engine.get_display())
            self.display_card.set_memory_active(self.scientific_engine.has_memory)

    # --- Physical Keyboard Support ---
    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        text = event.text()
        modifiers = event.modifiers()

        # Keyboard shortcuts with Ctrl
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            if key == Qt.Key.Key_1:
                self.mode_selector.set_active_mode(MODE_STANDARD)
                return
            elif key == Qt.Key.Key_2:
                self.mode_selector.set_active_mode(MODE_SCIENTIFIC)
                return
            elif key == Qt.Key.Key_3:
                self.mode_selector.set_active_mode(MODE_BUSINESS)
                return
            elif key == Qt.Key.Key_H:
                self._toggle_history()
                return
            elif key == Qt.Key.Key_C:
                # Copy current display
                QApplication.clipboard().setText(self.display_card.get_result())
                return
            elif key == Qt.Key.Key_V:
                # Paste clipboard text into calculator
                clipboard_text = QApplication.clipboard().text().strip()
                if clipboard_text:
                    if self.current_mode == MODE_STANDARD:
                        self.standard_engine.display_value = clipboard_text
                        self.standard_engine.is_new_entry = False
                        self._update_display_from_active_engine()
                    elif self.current_mode == MODE_SCIENTIFIC:
                        self.scientific_engine.display_value = clipboard_text
                        self.scientific_engine.is_new_entry = False
                        self._update_display_from_active_engine()
                return

        # Digits 0-9
        if text in "0123456789":
            if self.current_mode == MODE_STANDARD:
                self._on_standard_digit(text)
            elif self.current_mode == MODE_SCIENTIFIC:
                self._on_scientific_digit(text)
            return

        # Decimal point
        if text == ".":
            if self.current_mode == MODE_STANDARD:
                self._on_standard_decimal()
            elif self.current_mode == MODE_SCIENTIFIC:
                self._on_scientific_decimal()
            return

        # Operators
        if text in ("+", "-", "*", "/", "%", "^"):
            op_map = {"+": "+", "-": "−", "*": "×", "/": "÷", "%": "%", "^": "^"}
            op = op_map.get(text, text)
            if self.current_mode == MODE_STANDARD:
                self._on_standard_operator(op)
            elif self.current_mode == MODE_SCIENTIFIC:
                self._on_scientific_operator(op)
            return

        # Parentheses
        if text in ("(", ")"):
            if self.current_mode == MODE_STANDARD:
                self._on_standard_parenthesis(text)
            elif self.current_mode == MODE_SCIENTIFIC:
                self._on_scientific_parenthesis(text)
            return

        # Equals / Enter
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Equal):
            if self.current_mode == MODE_STANDARD:
                self._on_standard_equals()
            elif self.current_mode == MODE_SCIENTIFIC:
                self._on_scientific_equals()
            return

        # Backspace / Delete
        if key == Qt.Key.Key_Backspace:
            if self.current_mode == MODE_STANDARD:
                self._on_standard_backspace()
            elif self.current_mode == MODE_SCIENTIFIC:
                self._on_scientific_backspace()
            return

        # Escape -> Clear All (AC)
        if key == Qt.Key.Key_Escape:
            if self.current_mode == MODE_STANDARD:
                self._on_standard_clear_all()
            elif self.current_mode == MODE_SCIENTIFIC:
                self._on_scientific_clear_all()
            return

        # 'c' or 'C' -> Clear Entry
        if text.lower() == "c":
            if self.current_mode == MODE_STANDARD:
                self.standard_engine.clear_entry()
                self._update_display_from_active_engine()
            elif self.current_mode == MODE_SCIENTIFIC:
                self.scientific_engine.clear_entry()
                self._update_display_from_active_engine()
            return

        super().keyPressEvent(event)
