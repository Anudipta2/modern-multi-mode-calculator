"""Modern Apple-inspired Glass Display Component."""

from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QApplication,
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QCursor


class CalculatorDisplay(QFrame):
    """Large, readable, glassmorphism calculator display with dynamic font scaling."""

    copy_requested = Signal()
    angle_mode_toggled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DisplayCard")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 16)
        layout.setSpacing(6)

        # --- Top Status & Quick Action Row ---
        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        # Mode Badge
        self.mode_badge = QLabel("STANDARD")
        self.mode_badge.setProperty("class", "badge-label-info")
        top_row.addWidget(self.mode_badge)

        # Angle Mode Badge (for Scientific)
        self.angle_badge = QPushButton("DEG")
        self.angle_badge.setObjectName("AngleBadgeBtn")
        self.angle_badge.setProperty("class", "top-icon-btn")
        self.angle_badge.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.angle_badge.setToolTip("Click to toggle Angle Mode: DEG / RAD / GRAD")
        self.angle_badge.clicked.connect(self.angle_mode_toggled.emit)
        self.angle_badge.hide()
        top_row.addWidget(self.angle_badge)

        # Memory Indicator Badge
        self.memory_badge = QLabel("M")
        self.memory_badge.setProperty("class", "badge-label")
        self.memory_badge.setToolTip("Value stored in Memory")
        self.memory_badge.hide()
        top_row.addWidget(self.memory_badge)

        top_row.addStretch()

        # Copy Result Button
        self.copy_btn = QPushButton("📋 Copy")
        self.copy_btn.setProperty("class", "top-icon-btn")
        self.copy_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.copy_btn.setToolTip("Copy result to clipboard")
        self.copy_btn.clicked.connect(self._on_copy_clicked)
        top_row.addWidget(self.copy_btn)

        layout.addLayout(top_row)

        # --- Expression Line ---
        self.expr_label = QLabel("")
        self.expr_label.setObjectName("ExpressionLabel")
        self.expr_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.expr_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.expr_label)

        # --- Result Line with Dynamic Font Scaling ---
        self.result_label = QLabel("0")
        self.result_label.setObjectName("ResultLabel")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.result_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.result_label)

    def set_mode_badge(self, mode_name: str, show_angle: bool = False, angle_mode: str = "DEG"):
        """Update top badge for current calculator mode."""
        self.mode_badge.setText(mode_name.upper())
        if show_angle:
            self.angle_badge.setText(angle_mode)
            self.angle_badge.show()
        else:
            self.angle_badge.hide()

    def set_memory_active(self, active: bool):
        """Show or hide the 'M' memory badge."""
        if active:
            self.memory_badge.show()
        else:
            self.memory_badge.hide()

    def set_expression(self, expr: str):
        """Set the expression line text."""
        self.expr_label.setText(expr)

    def set_result(self, result_text: str):
        """Set the large result text and adjust font size dynamically."""
        self.result_label.setText(result_text)
        self._adjust_font_size(result_text)

    def _adjust_font_size(self, text: str):
        """Dynamically scale font size so large numbers or long errors never truncate."""
        length = len(text)
        font = self.result_label.font()

        if length <= 9:
            font.setPointSize(38)
        elif length <= 13:
            font.setPointSize(30)
        elif length <= 18:
            font.setPointSize(24)
        elif length <= 25:
            font.setPointSize(19)
        else:
            font.setPointSize(15)

        font.setWeight(QFont.Weight.Bold)
        self.result_label.setFont(font)

    def get_result(self) -> str:
        return self.result_label.text()

    def get_expression(self) -> str:
        return self.expr_label.text()

    def _on_copy_clicked(self):
        """Copy current result to system clipboard with visual feedback."""
        clipboard = QApplication.clipboard()
        text = self.result_label.text()
        clipboard.setText(text)
        self.copy_btn.setText("✓ Copied!")
        QTimer.singleShot(1500, lambda: self.copy_btn.setText("📋 Copy"))
        self.copy_requested.emit()
