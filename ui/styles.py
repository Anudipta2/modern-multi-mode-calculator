"""Apple-inspired dark glassmorphism stylesheet (QSS) and visual theme."""

GLASS_THEME_QSS = """
/* ==========================================================================
   GLOBAL APP STYLING
   ========================================================================== */
QWidget#CentralWidget {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #121316,
        stop: 0.5 #16181D,
        stop: 1 #1A1C22
    );
    color: #F5F5F7;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI Variable Display", "Segoe UI", Roboto, sans-serif;
}

QMainWindow {
    background-color: #121316;
}

QToolTip {
    background-color: rgba(30, 32, 40, 0.95);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}

/* ==========================================================================
   TOP BAR & MODE SELECTOR
   ========================================================================== */
QFrame#TopBarFrame {
    background-color: rgba(25, 27, 34, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    padding: 4px;
}

QFrame#SegmentedControl {
    background-color: rgba(18, 19, 24, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 3px;
}

QPushButton.mode-pill {
    background-color: transparent;
    color: #989BA5;
    border: none;
    border-radius: 9px;
    font-size: 13px;
    font-weight: 600;
    padding: 8px 18px;
    min-height: 20px;
}

QPushButton.mode-pill:hover {
    color: #FFFFFF;
    background-color: rgba(255, 255, 255, 0.05);
}

QPushButton.mode-pill:checked {
    background-color: rgba(255, 255, 255, 0.15);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.18);
}

/* Icon Buttons on Top Bar (History, Copy, Angle) */
QPushButton.top-icon-btn {
    background-color: rgba(255, 255, 255, 0.06);
    color: #D1D5DB;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 12px;
    min-height: 22px;
}

QPushButton.top-icon-btn:hover {
    background-color: rgba(255, 255, 255, 0.12);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.18);
}

QPushButton.top-icon-btn:pressed {
    background-color: rgba(255, 255, 255, 0.20);
}

QPushButton.top-icon-btn:checked {
    background-color: rgba(255, 159, 10, 0.25);
    color: #FF9F0A;
    border: 1px solid rgba(255, 159, 10, 0.45);
}

/* ==========================================================================
   DISPLAY CARD
   ========================================================================== */
QFrame#DisplayCard {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 rgba(28, 30, 38, 0.85),
        stop: 1 rgba(20, 22, 28, 0.90)
    );
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 20px;
    padding: 16px 20px;
}

QLabel#ExpressionLabel {
    color: #8E92A0;
    font-size: 16px;
    font-weight: 500;
    letter-spacing: 0.5px;
}

QLabel#ResultLabel {
    color: #FFFFFF;
    font-size: 42px;
    font-weight: 700;
    letter-spacing: -0.5px;
}

QLabel.badge-label {
    background-color: rgba(255, 159, 10, 0.18);
    color: #FF9F0A;
    border: 1px solid rgba(255, 159, 10, 0.35);
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 11px;
    font-weight: 700;
}

QLabel.badge-label-info {
    background-color: rgba(10, 132, 255, 0.18);
    color: #0A84FF;
    border: 1px solid rgba(10, 132, 255, 0.35);
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 11px;
    font-weight: 700;
}

/* ==========================================================================
   CALCULATOR BUTTONS
   ========================================================================== */
/* Common base */
QPushButton.calc-btn {
    border-radius: 16px;
    font-size: 19px;
    font-weight: 600;
    min-height: 52px;
    min-width: 52px;
    outline: none;
}

/* 1. Number Buttons (0-9, decimal) */
QPushButton.btn-number {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 rgba(52, 56, 68, 0.85),
        stop: 1 rgba(40, 43, 53, 0.90)
    );
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

QPushButton.btn-number:hover {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 rgba(68, 73, 88, 0.92),
        stop: 1 rgba(54, 58, 70, 0.95)
    );
    border: 1px solid rgba(255, 255, 255, 0.18);
}

QPushButton.btn-number:pressed {
    background-color: rgba(30, 32, 40, 0.98);
}

/* 2. Utility / Function Buttons (AC, ±, %, Parentheses, ⌫) */
QPushButton.btn-util {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 rgba(74, 80, 98, 0.70),
        stop: 1 rgba(58, 63, 78, 0.75)
    );
    color: #E6E8F0;
    border: 1px solid rgba(255, 255, 255, 0.10);
    font-size: 17px;
}

QPushButton.btn-util:hover {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 rgba(92, 99, 120, 0.85),
        stop: 1 rgba(74, 80, 98, 0.90)
    );
    border: 1px solid rgba(255, 255, 255, 0.22);
    color: #FFFFFF;
}

QPushButton.btn-util:pressed {
    background-color: rgba(45, 48, 60, 0.95);
}

/* 3. Memory Buttons */
QPushButton.btn-memory {
    background-color: rgba(45, 48, 60, 0.50);
    color: #A5A9B8;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    font-size: 13px;
    font-weight: 700;
    min-height: 38px;
}

QPushButton.btn-memory:hover {
    background-color: rgba(65, 70, 85, 0.70);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.15);
}

QPushButton.btn-memory:pressed {
    background-color: rgba(35, 38, 48, 0.85);
}

/* 4. Operator Buttons (+, −, ×, ÷) */
QPushButton.btn-operator {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #FF9F0A,
        stop: 1 #E68A00
    );
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.20);
    font-size: 22px;
}

QPushButton.btn-operator:hover {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #FFB340,
        stop: 1 #FF9F0A
    );
    border: 1px solid rgba(255, 255, 255, 0.35);
}

QPushButton.btn-operator:pressed {
    background-color: #CC7A00;
}

/* 5. Equals Button (=) */
QPushButton.btn-equals {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #30D158,
        stop: 1 #24B045
    );
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.25);
    font-size: 24px;
    font-weight: 700;
}

QPushButton.btn-equals:hover {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #3CE467,
        stop: 1 #30D158
    );
    border: 1px solid rgba(255, 255, 255, 0.40);
}

QPushButton.btn-equals:pressed {
    background-color: #1E9E3B;
}

/* 6. Scientific Function Buttons (sin, cos, tan, ln, log, sqrt, etc.) */
QPushButton.btn-scientific {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 rgba(42, 45, 56, 0.75),
        stop: 1 rgba(32, 35, 44, 0.80)
    );
    color: #CFD3E2;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    font-size: 14px;
    font-weight: 600;
    min-height: 44px;
}

QPushButton.btn-scientific:hover {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 rgba(60, 65, 80, 0.88),
        stop: 1 rgba(46, 50, 62, 0.90)
    );
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.20);
}

QPushButton.btn-scientific:pressed {
    background-color: rgba(25, 27, 34, 0.95);
}

/* ==========================================================================
   BUSINESS VIEW STYLING
   ========================================================================== */
QFrame#BusinessCard {
    background-color: rgba(26, 28, 36, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 18px;
    padding: 16px;
}

QTabWidget::pane {
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    background-color: rgba(24, 26, 33, 0.70);
    padding: 12px;
}

QTabBar::tab {
    background-color: rgba(35, 38, 48, 0.60);
    color: #A5A9B8;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 9px 16px;
    margin-right: 6px;
    margin-bottom: 8px;
    font-size: 13px;
    font-weight: 600;
}

QTabBar::tab:hover {
    background-color: rgba(55, 60, 75, 0.75);
    color: #FFFFFF;
}

QTabBar::tab:selected {
    background-color: rgba(255, 159, 10, 0.22);
    color: #FF9F0A;
    border: 1px solid rgba(255, 159, 10, 0.45);
}

/* Inputs in Business View */
QLineEdit.business-input {
    background-color: rgba(18, 20, 26, 0.85);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 10px 14px;
    font-size: 16px;
    font-weight: 500;
    selection-background-color: #FF9F0A;
}

QLineEdit.business-input:focus {
    border: 1.5px solid #FF9F0A;
    background-color: rgba(22, 25, 33, 0.95);
}

QComboBox.business-combo {
    background-color: rgba(30, 33, 42, 0.85);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 8px 14px;
    font-size: 14px;
    font-weight: 500;
}

QComboBox.business-combo::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #1E2028;
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 8px;
    selection-background-color: #FF9F0A;
}

/* Primary Action Buttons */
QPushButton.btn-action-primary {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #FF9F0A,
        stop: 1 #E68A00
    );
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 12px;
    font-size: 15px;
    font-weight: 700;
    padding: 10px 20px;
    min-height: 24px;
}

QPushButton.btn-action-primary:hover {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #FFB340,
        stop: 1 #FF9F0A
    );
    border: 1px solid rgba(255, 255, 255, 0.40);
}

QPushButton.btn-action-primary:pressed {
    background-color: #CC7A00;
}

/* Secondary Action Buttons (e.g. Copy, Clear) */
QPushButton.btn-action-secondary {
    background-color: rgba(255, 255, 255, 0.08);
    color: #E2E4EB;
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 10px;
    font-size: 13px;
    font-weight: 600;
    padding: 7px 14px;
}

QPushButton.btn-action-secondary:hover {
    background-color: rgba(255, 255, 255, 0.16);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.20);
}

/* Results Display Box in Business View */
QFrame#BusinessResultFrame {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 rgba(22, 25, 33, 0.90),
        stop: 1 rgba(30, 34, 46, 0.90)
    );
    border: 1px solid rgba(255, 159, 10, 0.25);
    border-radius: 16px;
    padding: 14px 18px;
}

QLabel.result-value-highlight {
    color: #FF9F0A;
    font-size: 26px;
    font-weight: 700;
}

/* ==========================================================================
   HISTORY DRAWER PANEL
   ========================================================================== */
QFrame#HistoryPanel {
    background-color: rgba(20, 22, 28, 0.95);
    border-left: 1px solid rgba(255, 255, 255, 0.10);
    border-top-left-radius: 20px;
    border-bottom-left-radius: 20px;
    padding: 16px;
}

QScrollArea {
    border: none;
    background: transparent;
}

QScrollBar:vertical {
    background: transparent;
    width: 6px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.20);
    min-height: 24px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(255, 255, 255, 0.35);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QFrame.history-entry-card {
    background-color: rgba(35, 38, 48, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 10px 14px;
}

QFrame.history-entry-card:hover {
    background-color: rgba(50, 54, 68, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.15);
}
"""
