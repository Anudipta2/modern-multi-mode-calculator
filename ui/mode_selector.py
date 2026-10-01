"""Top Navigation bar and segmented mode selector component."""

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QPushButton,
    QButtonGroup,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from core.constants import MODE_STANDARD, MODE_SCIENTIFIC, MODE_BUSINESS


class ModeSelector(QFrame):
    """Modern macOS / iOS style segmented control for calculator modes."""

    mode_changed = Signal(str)
    history_toggled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TopBarFrame")
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(10)

        # Segmented Control Container
        seg_frame = QFrame()
        seg_frame.setObjectName("SegmentedControl")
        seg_layout = QHBoxLayout(seg_frame)
        seg_layout.setContentsMargins(3, 3, 3, 3)
        seg_layout.setSpacing(4)

        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        self.btn_standard = QPushButton("Standard")
        self.btn_standard.setProperty("class", "mode-pill")
        self.btn_standard.setCheckable(True)
        self.btn_standard.setChecked(True)
        self.btn_standard.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_standard.setToolTip("Standard everyday arithmetic (Ctrl+1)")

        self.btn_scientific = QPushButton("Scientific")
        self.btn_scientific.setProperty("class", "mode-pill")
        self.btn_scientific.setCheckable(True)
        self.btn_scientific.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_scientific.setToolTip("Advanced scientific & engineering functions (Ctrl+2)")

        self.btn_business = QPushButton("Business")
        self.btn_business.setProperty("class", "mode-pill")
        self.btn_business.setCheckable(True)
        self.btn_business.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_business.setToolTip("Financial tools, GST, EMI, Interest, Profit & Loss (Ctrl+3)")

        self.btn_group.addButton(self.btn_standard, 0)
        self.btn_group.addButton(self.btn_scientific, 1)
        self.btn_group.addButton(self.btn_business, 2)

        self.btn_standard.clicked.connect(lambda: self.mode_changed.emit(MODE_STANDARD))
        self.btn_scientific.clicked.connect(lambda: self.mode_changed.emit(MODE_SCIENTIFIC))
        self.btn_business.clicked.connect(lambda: self.mode_changed.emit(MODE_BUSINESS))

        seg_layout.addWidget(self.btn_standard)
        seg_layout.addWidget(self.btn_scientific)
        seg_layout.addWidget(self.btn_business)

        layout.addWidget(seg_frame)
        layout.addStretch()

        # History Drawer Toggle Button
        self.history_btn = QPushButton("🕒 History")
        self.history_btn.setProperty("class", "top-icon-btn")
        self.history_btn.setCheckable(True)
        self.history_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.history_btn.setToolTip("Toggle calculation history panel (Ctrl+H)")
        self.history_btn.clicked.connect(self.history_toggled.emit)

        layout.addWidget(self.history_btn)

    def set_active_mode(self, mode: str):
        """Programmatically switch active mode."""
        if mode == MODE_STANDARD:
            self.btn_standard.setChecked(True)
        elif mode == MODE_SCIENTIFIC:
            self.btn_scientific.setChecked(True)
        elif mode == MODE_BUSINESS:
            self.btn_business.setChecked(True)
        self.mode_changed.emit(mode)

    def set_history_active(self, active: bool):
        self.history_btn.setChecked(active)
