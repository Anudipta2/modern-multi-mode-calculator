"""Luxury Minimalist Glass Title Bar with Apple-style micro-traffic light controls."""

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QPushButton,
    QLabel,
)
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QCursor


class GlassTitleBar(QFrame):
    """Sleek, luxury minimalist glass title bar with Apple-style window controls."""

    close_clicked = Signal()
    minimize_clicked = Signal()
    maximize_clicked = Signal()
    opacity_cycle_clicked = Signal()
    pin_toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("GlassTitleBar")
        self.is_pinned = False
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 2)
        layout.setSpacing(10)

        # 1. Apple-style Traffic Light Controls (Close, Min, Max)
        traffic_layout = QHBoxLayout()
        traffic_layout.setSpacing(8)

        self.btn_close = QPushButton("✕")
        self.btn_close.setProperty("class", "traffic-close")
        self.btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_close.setToolTip("Close")
        self.btn_close.clicked.connect(self.close_clicked.emit)

        self.btn_min = QPushButton("−")
        self.btn_min.setProperty("class", "traffic-min")
        self.btn_min.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_min.setToolTip("Minimize")
        self.btn_min.clicked.connect(self.minimize_clicked.emit)

        self.btn_max = QPushButton("⤢")
        self.btn_max.setProperty("class", "traffic-max")
        self.btn_max.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_max.setToolTip("Maximize / Restore")
        self.btn_max.clicked.connect(self.maximize_clicked.emit)

        traffic_layout.addWidget(self.btn_close)
        traffic_layout.addWidget(self.btn_min)
        traffic_layout.addWidget(self.btn_max)
        layout.addLayout(traffic_layout)

        # 2. Minimalist Center Title
        layout.addSpacing(8)
        self.title_label = QLabel("CALCULATOR")
        self.title_label.setObjectName("GlassTitleLabel")
        layout.addWidget(self.title_label)

        layout.addStretch()

        # 3. Translucency Selector
        self.btn_opacity = QPushButton("Glass 40%")
        self.btn_opacity.setProperty("class", "header-pill-btn")
        self.btn_opacity.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_opacity.setToolTip("Cycle transparency level: 25% / 40% / 60%")
        self.btn_opacity.clicked.connect(self.opacity_cycle_clicked.emit)
        layout.addWidget(self.btn_opacity)

        # 4. Always On Top Pin
        self.btn_pin = QPushButton("Pin")
        self.btn_pin.setProperty("class", "header-pill-btn")
        self.btn_pin.setCheckable(True)
        self.btn_pin.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_pin.setToolTip("Keep calculator floating on top of all windows")
        self.btn_pin.clicked.connect(self._on_pin_clicked)
        layout.addWidget(self.btn_pin)

    def set_opacity_text(self, text: str):
        self.btn_opacity.setText(text)

    def _on_pin_clicked(self, checked: bool):
        self.is_pinned = checked
        self.btn_pin.setChecked(checked)
        self.pin_toggled.emit(checked)
