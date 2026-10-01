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
