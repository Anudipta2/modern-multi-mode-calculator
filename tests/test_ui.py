"""Integration tests for PySide6 UI components and mode transitions."""

import sys
import pytest
from PySide6.QtWidgets import QApplication
from ui.main_window import ModernCalculatorWindow
from core.constants import MODE_STANDARD, MODE_SCIENTIFIC, MODE_BUSINESS


@pytest.fixture(scope="session")
def qapp():
    """Ensure QApplication instance is created for the test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


def test_main_window_modes(qapp):
    win = ModernCalculatorWindow()
    win.show()
    assert win.current_mode == MODE_STANDARD
    assert not win.display_card.isHidden()

    # Switch to Scientific
    win.set_mode(MODE_SCIENTIFIC)
    assert win.current_mode == MODE_SCIENTIFIC
    assert not win.display_card.isHidden()
    assert not win.display_card.angle_badge.isHidden()

    # Switch to Business
    win.set_mode(MODE_BUSINESS)
    assert win.current_mode == MODE_BUSINESS
    assert win.display_card.isHidden()

    # Switch back to Standard
    win.set_mode(MODE_STANDARD)
    assert win.current_mode == MODE_STANDARD
    assert not win.display_card.isHidden()
    win.close()


def test_standard_keypad_interactions(qapp):
    win = ModernCalculatorWindow()
    # Digits: 1, 2, 5
    win._on_standard_digit("1")
    win._on_standard_digit("2")
    win._on_standard_digit("5")
    assert win.display_card.get_result() == "125"

    # Operator +
    win._on_standard_operator("+")
    assert win.display_card.get_expression() == "125 +"

    # Digits: 2, 5
    win._on_standard_digit("2")
    win._on_standard_digit("5")
    assert win.display_card.get_result() == "25"

    # Equals
    win._on_standard_equals()
    assert win.display_card.get_result() == "150"

    win.close()


def test_scientific_keypad_interactions(qapp):
    win = ModernCalculatorWindow()
    win.set_mode(MODE_SCIENTIFIC)

    # 144 -> sqrt -> 12
    win._on_scientific_digit("1")
    win._on_scientific_digit("4")
    win._on_scientific_digit("4")
    win._on_scientific_unary("sqrt")
    assert win.display_card.get_result() == "12"

    win.close()


def test_history_drawer_toggle(qapp):
    win = ModernCalculatorWindow()
    win.show()
    assert win.history_panel.isHidden()

    win._toggle_history()
    assert not win.history_panel.isHidden()

    win._toggle_history()
    assert win.history_panel.isHidden()
    win.close()


def test_business_view_calculations(qapp):
    win = ModernCalculatorWindow()
    win.set_mode(MODE_BUSINESS)

    bv = win.business_view
    bv.gst_amount_input.setText("5000")
    bv.gst_custom_rate.setText("18")
    bv._calculate_gst()

    assert "Final Total:" in bv.gst_final_label.text()
    assert "5,900" in bv.gst_final_label.text()
    win.close()


def test_percentage_ui_flow(qapp):
    win = ModernCalculatorWindow()
    win.set_mode(MODE_STANDARD)

    # 100 * 50% = 50
    win._on_standard_digit("1")
    win._on_standard_digit("0")
    win._on_standard_digit("0")
    win._on_standard_operator("×")
    win._on_standard_digit("5")
    win._on_standard_digit("0")
    win._on_standard_percentage()
    assert win.display_card.get_result() == "0.5"

    win._on_standard_equals()
    assert win.display_card.get_result() == "50"
    win.close()


def test_percentage_keyboard_event(qapp):
    from PySide6.QtGui import QKeyEvent
    from PySide6.QtCore import QEvent, Qt

    win = ModernCalculatorWindow()
    win.set_mode(MODE_STANDARD)

    # Simulate keyboard typing: 1, 0, 0, *, 5, 0, %
    win.keyPressEvent(QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_1, Qt.KeyboardModifier.NoModifier, "1"))
    win.keyPressEvent(QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_0, Qt.KeyboardModifier.NoModifier, "0"))
    win.keyPressEvent(QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_0, Qt.KeyboardModifier.NoModifier, "0"))
    win.keyPressEvent(QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Asterisk, Qt.KeyboardModifier.NoModifier, "*"))
    win.keyPressEvent(QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_5, Qt.KeyboardModifier.NoModifier, "5"))
    win.keyPressEvent(QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_0, Qt.KeyboardModifier.NoModifier, "0"))
    win.keyPressEvent(QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Percent, Qt.KeyboardModifier.NoModifier, "%"))

    assert win.display_card.get_result() == "0.5"

    win.keyPressEvent(QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Return, Qt.KeyboardModifier.NoModifier, "\r"))
    assert win.display_card.get_result() == "50"
    win.close()


def test_glass_title_bar_controls(qapp):
    win = ModernCalculatorWindow()
    win.show()

    # Verify glass title bar is present and configured
    assert win.title_bar is not None
    assert "40%" in win.title_bar.btn_opacity.text()

    # Cycle opacity presets: 40% -> 60% -> 25% -> 40%
    win._cycle_glass_opacity()
    assert "60%" in win.title_bar.btn_opacity.text()

    win._cycle_glass_opacity()
    assert "25%" in win.title_bar.btn_opacity.text()

    win._cycle_glass_opacity()
    assert "40%" in win.title_bar.btn_opacity.text()

    # Toggle Pin
    win.title_bar.btn_pin.click()
    assert win.title_bar.is_pinned is True

    win.title_bar.btn_pin.click()
    assert win.title_bar.is_pinned is False

    win.close()


