"""Calculation History drawer panel component."""

from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QWidget,
    QComboBox,
    QApplication,
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QCursor
from core.history import HistoryManager


class HistoryPanel(QFrame):
    """Sleek collapsible glass panel displaying calculation history with interactive reuse."""

    entry_selected = Signal(str)  # result selected to reuse
    close_requested = Signal()

    def __init__(self, history_manager: HistoryManager, parent=None):
        super().__init__(parent)
        self.history_manager = history_manager
        self.setObjectName("HistoryPanel")
        self.setMinimumWidth(320)
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(10)

        # Header Row
        header_layout = QHBoxLayout()
        title = QLabel("Calculation History")
        title.setStyleSheet("font-size: 16px; font-weight: 700; color: #FFFFFF;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setProperty("class", "top-icon-btn")
        close_btn.setMaximumWidth(32)
        close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        close_btn.clicked.connect(self.close_requested.emit)
        header_layout.addWidget(close_btn)
        main_layout.addLayout(header_layout)

        # Filter row
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter:")
        filter_label.setStyleSheet("color: #989BA5; font-size: 12px; font-weight: 600;")
        filter_layout.addWidget(filter_label)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Modes", "Standard", "Scientific", "Business"])
        self.filter_combo.setProperty("class", "business-combo")
        self.filter_combo.currentIndexChanged.connect(self.refresh)
        filter_layout.addWidget(self.filter_combo)
        main_layout.addLayout(filter_layout)

        # Scrollable list of entries
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.entries_layout = QVBoxLayout(self.scroll_content)
        self.entries_layout.setContentsMargins(0, 0, 4, 0)
        self.entries_layout.setSpacing(8)
        self.entries_layout.addStretch()
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)

        # Footer Actions
        footer_layout = QHBoxLayout()
        clear_btn = QPushButton("🗑️ Clear History")
        clear_btn.setProperty("class", "btn-action-secondary")
        clear_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        clear_btn.clicked.connect(self._clear_all)
        footer_layout.addWidget(clear_btn)
        main_layout.addLayout(footer_layout)

        self.refresh()

    def refresh(self):
        """Rebuild the history items list from the history manager."""
        # Clear existing widgets
        while self.entries_layout.count() > 1:
            item = self.entries_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        filter_text = self.filter_combo.currentText().lower()
        mode_filter = None if filter_text == "all modes" else filter_text

        entries = self.history_manager.get_entries(mode=mode_filter)

        if not entries:
            empty_lbl = QLabel("No calculation history yet.")
            empty_lbl.setStyleSheet("color: #717684; font-size: 13px; padding: 20px; font-style: italic;")
            empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.entries_layout.insertWidget(0, empty_lbl)
            return

        for idx, entry in enumerate(entries):
            card = self._create_entry_card(idx, entry)
            self.entries_layout.insertWidget(idx, card)

    def _create_entry_card(self, index: int, entry: dict) -> QFrame:
        card = QFrame()
        card.setProperty("class", "history-entry-card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        # Metadata Row (Mode & Timestamp)
        meta_layout = QHBoxLayout()
        mode_badge = QLabel(entry.get("mode", "calc").upper())
        mode_badge.setStyleSheet("color: #FF9F0A; font-size: 10px; font-weight: 700; background: rgba(255, 159, 10, 0.15); padding: 1px 5px; border-radius: 4px;")
        time_lbl = QLabel(entry.get("timestamp", ""))
        time_lbl.setStyleSheet("color: #6B7280; font-size: 11px;")
        meta_layout.addWidget(mode_badge)
        meta_layout.addWidget(time_lbl)
        meta_layout.addStretch()
        layout.addLayout(meta_layout)

        # Expression
        expr_lbl = QLabel(entry.get("expression", ""))
        expr_lbl.setStyleSheet("color: #9CA3AF; font-size: 13px;")
        expr_lbl.setWordWrap(True)
        layout.addWidget(expr_lbl)

        # Result
        res_lbl = QLabel(f"= {entry.get('result', '')}")
        res_lbl.setStyleSheet("color: #FFFFFF; font-size: 17px; font-weight: 700;")
        res_lbl.setWordWrap(True)
        layout.addWidget(res_lbl)

        # Action Buttons
        btn_layout = QHBoxLayout()
        use_btn = QPushButton("Reuse")
        use_btn.setProperty("class", "btn-action-secondary")
        use_btn.setStyleSheet("font-size: 11px; padding: 3px 8px;")
        use_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        use_btn.clicked.connect(lambda _, r=entry.get("result", ""): self.entry_selected.emit(r))

        copy_btn = QPushButton("Copy")
        copy_btn.setProperty("class", "btn-action-secondary")
        copy_btn.setStyleSheet("font-size: 11px; padding: 3px 8px;")
        copy_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        copy_btn.clicked.connect(lambda _, r=entry.get("result", ""), b=copy_btn: self._copy_result(r, b))

        del_btn = QPushButton("✕")
        del_btn.setProperty("class", "btn-action-secondary")
        del_btn.setStyleSheet("font-size: 11px; padding: 3px 8px; color: #FF453A;")
        del_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        del_btn.clicked.connect(lambda _, i=index: self._delete_entry(i))

        btn_layout.addWidget(use_btn)
        btn_layout.addWidget(copy_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(del_btn)
        layout.addLayout(btn_layout)

        return card

    def _copy_result(self, result: str, btn: QPushButton):
        QApplication.clipboard().setText(result)
        btn.setText("✓")
        QTimer.singleShot(1200, lambda: btn.setText("Copy"))

    def _delete_entry(self, index: int):
        self.history_manager.remove_entry(index)
        self.refresh()

    def _clear_all(self):
        self.history_manager.clear()
        self.refresh()
