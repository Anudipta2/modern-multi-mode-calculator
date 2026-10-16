"""Master MainWindow integrating Display, Keypads, Business View, and History Drawer.

Features:
- Full transparent physical optical glass body with Windows 11 Acrylic blur
- Apple-inspired glass traffic light controls (close, minimize, maximize)
- Smooth window dragging and edge resizing for frameless glass aesthetic
- Translucency level switcher (30% Ultra-Clear / 45% Crystal Glass / 65% Smoked Glass)
- Always-on-top window pin
"""

import os
import sys

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QApplication,
    QFrame,
    QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QKeyEvent, QKeySequence, QIcon, QMouseEvent, QColor

from core.constants import MODE_STANDARD, MODE_SCIENTIFIC, MODE_BUSINESS
from core.history import HistoryManager
from calculators.standard import StandardCalculatorEngine
from calculators.scientific import ScientificCalculatorEngine
from calculators.business import BusinessCalculatorEngine

from ui.styles import GLASS_THEME_QSS, get_glass_theme
from ui.title_bar import GlassTitleBar
from ui.mode_selector import ModeSelector
from ui.calculator_display import CalculatorDisplay
from ui.keypad import StandardKeypad, ScientificKeypad
from ui.business_view import BusinessView
from ui.history_panel import HistoryPanel


class ModernCalculatorWindow(QMainWindow):
    """Main Application Window for the Physical Glass Modern Multi-Mode Calculator."""

    EDGE_NONE = 0
    EDGE_LEFT = 1
    EDGE_TOP = 2
    EDGE_RIGHT = 4
    EDGE_BOTTOM = 8

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Multi-Mode Calculator")

        # Dynamically adapt to screen dimensions and Windows taskbar
        screen = QApplication.primaryScreen()
        avail = screen.availableGeometry() if screen else None
        avail_w = avail.width() if avail else 1280
        avail_h = avail.height() if avail else 800

        # Dynamic constraints supporting screens down to 1024x600 and up to 4K
        min_w = min(360, int(avail_w * 0.90))
        min_h = min(530, int(avail_h * 0.85))
        self.setMinimumSize(min_w, min_h)

        # Default size bounded within current screen resolution
        init_w = min(490, int(avail_w * 0.85))
        init_h = min(690, int(avail_h * 0.88))
        self.resize(init_w, init_h)

        # Enable full transparent frameless window for true glassmorphism
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setMouseTracking(True)

        # Initialize Data & Calculation Engines
        self.history_manager = HistoryManager()
        self.standard_engine = StandardCalculatorEngine()
        self.scientific_engine = ScientificCalculatorEngine()
        self.business_engine = BusinessCalculatorEngine()

        self.current_mode = MODE_STANDARD

        # Dragging and Resizing State
        self._is_dragging = False
        self._drag_start_pos = QPoint()
        self._is_resizing = False
        self._resize_edge = self.EDGE_NONE
        self._resize_start_geom = None
        self._resize_start_global = None

        # Opacity Presets (Level, Label)
        self.opacity_presets = [
            (0.25, "Glass 25%"),  # Ultra Clear
            (0.40, "Glass 40%"),  # Crystal Glass (Default)
            (0.60, "Glass 60%"),  # Smoked Glass
        ]
        self.current_opacity_idx = 1

        # Set Window Icon
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(base_dir, "assets", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Apply Global Physical Glass Theme
        self.setStyleSheet(get_glass_theme(self.opacity_presets[self.current_opacity_idx][0]))

        self._init_ui()
        self._wire_signals()
        self._update_display_from_active_engine()

    def showEvent(self, event):
        super().showEvent(event)
        self._enable_windows_acrylic()

    def _enable_windows_acrylic(self):
        """Enable Windows 11 Acrylic blur or DWM backdrop on the HWND."""
        if sys.platform != "win32":
            return
        try:
            hwnd = int(self.winId())
            import ctypes
            from ctypes import wintypes, byref, sizeof, c_int, Structure, POINTER

            # Windows 11 DWM backdrop
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            DWMWA_SYSTEMBACKDROP_TYPE = 38
            DWMSBT_TRANSIENTWINDOW = 3  # Acrylic blur behind

            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, byref(c_int(1)), sizeof(c_int)
            )
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_SYSTEMBACKDROP_TYPE, byref(c_int(DWMSBT_TRANSIENTWINDOW)), sizeof(c_int)
            )

            # SetWindowCompositionAttribute Acrylic / BlurBehind fallback
            class ACCENT_POLICY(Structure):
                _fields_ = [
                    ('AccentState', c_int),
                    ('AccentFlags', c_int),
                    ('GradientColor', c_int),
                    ('AnimationId', c_int)
                ]

            class WINDOWCOMPOSITIONATTRIBDATA(Structure):
                _fields_ = [
                    ('Attribute', c_int),
                    ('Data', POINTER(ACCENT_POLICY)),
                    ('SizeOfData', c_int)
                ]

            user32 = ctypes.windll.user32
            SetWindowCompositionAttribute = getattr(user32, 'SetWindowCompositionAttribute', None)
            if SetWindowCompositionAttribute:
                accent = ACCENT_POLICY()
                accent.AccentState = 4  # ACCENT_ENABLE_ACRYLICBLURBEHIND
                accent.AccentFlags = 2
                accent.GradientColor = 0x01141824  # Subtle dark ARGB tint
                accent.AnimationId = 0

                data = WINDOWCOMPOSITIONATTRIBDATA()
                data.Attribute = 19  # WCA_ACCENT_POLICY
                data.Data = ctypes.pointer(accent)
                data.SizeOfData = sizeof(accent)
                SetWindowCompositionAttribute(hwnd, ctypes.byref(data))
        except Exception:
            pass

    def _init_ui(self):
        # Outer transparent central widget with shadow padding
        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        central_widget.setMouseTracking(True)
        self.setCentralWidget(central_widget)

        window_layout = QVBoxLayout(central_widget)
        window_layout.setContentsMargins(10, 10, 10, 10)
        window_layout.setSpacing(0)

        # The Master Physical Glass Frame (with beveled edges and ambient shadow)
        self.glass_frame = QFrame()
        self.glass_frame.setObjectName("GlassWindowFrame")
        self.glass_frame.setMouseTracking(True)

        # Ambient Occlusion Drop Shadow on the desktop
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(36)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 12)
        self.glass_frame.setGraphicsEffect(shadow)

        glass_layout = QVBoxLayout(self.glass_frame)
        glass_layout.setContentsMargins(14, 12, 14, 14)
        glass_layout.setSpacing(10)

        # 1. Apple-Style Glass Title Bar
        self.title_bar = GlassTitleBar(self)
        glass_layout.addWidget(self.title_bar)

        # Content Layout (Calculator column + History drawer)
        content_container = QWidget()
        content_container.setMouseTracking(True)
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        # Left / Main Calculator Column
        self.main_calc_widget = QWidget()
        self.main_calc_widget.setMouseTracking(True)
        calc_layout = QVBoxLayout(self.main_calc_widget)
        calc_layout.setContentsMargins(0, 0, 0, 0)
        calc_layout.setSpacing(12)

        # 2. Top Bar Mode Selector
        self.mode_selector = ModeSelector()
        calc_layout.addWidget(self.mode_selector)

        # 3. Glass Display Card
        self.display_card = CalculatorDisplay()
        calc_layout.addWidget(self.display_card)

        # 4. Stacked Keypads / Views
        self.stack = QStackedWidget()

        self.standard_keypad = StandardKeypad()
        self.scientific_keypad = ScientificKeypad()
        self.business_view = BusinessView(self.business_engine)

        self.stack.addWidget(self.standard_keypad)    # Index 0
        self.stack.addWidget(self.scientific_keypad)  # Index 1
        self.stack.addWidget(self.business_view)      # Index 2

        calc_layout.addWidget(self.stack, 1)

        content_layout.addWidget(self.main_calc_widget, 1)

        # 5. Collapsible History Drawer on the Right
        self.history_panel = HistoryPanel(self.history_manager)
        self.history_panel.hide()
        content_layout.addWidget(self.history_panel)

        glass_layout.addWidget(content_container, 1)
        window_layout.addWidget(self.glass_frame)

    def _wire_signals(self):
        # Title bar controls
        self.title_bar.close_clicked.connect(self.close)
        self.title_bar.minimize_clicked.connect(self.showMinimized)
        self.title_bar.maximize_clicked.connect(self.toggle_maximize)
        self.title_bar.opacity_cycle_clicked.connect(self._cycle_glass_opacity)
        self.title_bar.pin_toggled.connect(self._toggle_always_on_top)

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

    def toggle_maximize(self):
        """Toggle maximize and restore states."""
        if self.isFullScreen():
            self.showNormal()
        elif self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def toggle_fullscreen(self):
        """Toggle true fullscreen state (F11)."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _cycle_glass_opacity(self):
        """Cycle through transparency presets (30% -> 45% -> 65%)."""
        self.current_opacity_idx = (self.current_opacity_idx + 1) % len(self.opacity_presets)
        level, label = self.opacity_presets[self.current_opacity_idx]
        self.title_bar.set_opacity_text(label)
        self.setStyleSheet(get_glass_theme(level))

    def _toggle_always_on_top(self, pinned: bool):
        """Keep the glass calculator floating above all windows."""
        was_visible = self.isVisible()
        flags = self.windowFlags()
        if pinned:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        else:
            flags &= ~Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        if was_visible:
            self.show()
            self._enable_windows_acrylic()

    # --- Frameless Mouse Dragging & Resizing ---
    def _detect_edge(self, pos: QPoint) -> int:
        if self.isMaximized():
            return self.EDGE_NONE
        m = 12
        edge = self.EDGE_NONE
        if pos.x() <= m:
            edge |= self.EDGE_LEFT
        elif pos.x() >= self.width() - m:
            edge |= self.EDGE_RIGHT
        if pos.y() <= m:
            edge |= self.EDGE_TOP
        elif pos.y() >= self.height() - m:
            edge |= self.EDGE_BOTTOM
        return edge

    def _update_cursor_for_edge(self, edge: int):
        if edge in (self.EDGE_LEFT | self.EDGE_TOP, self.EDGE_RIGHT | self.EDGE_BOTTOM):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif edge in (self.EDGE_RIGHT | self.EDGE_TOP, self.EDGE_LEFT | self.EDGE_BOTTOM):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif edge in (self.EDGE_LEFT, self.EDGE_RIGHT):
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif edge in (self.EDGE_TOP, self.EDGE_BOTTOM):
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        else:
            self.unsetCursor()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            edge = self._detect_edge(pos)
            if edge != self.EDGE_NONE:
                self._is_resizing = True
                self._resize_edge = edge
                self._resize_start_geom = self.geometry()
                self._resize_start_global = event.globalPosition().toPoint()
                event.accept()
                return

            child = self.childAt(pos)
            if child in (self, self.centralWidget(), self.glass_frame, self.title_bar, self.title_bar.title_label):
                self._is_dragging = True
                self._drag_start_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = event.position().toPoint()
        global_pos = event.globalPosition().toPoint()
        if self._is_dragging:
            self.move(global_pos - self._drag_start_pos)
            event.accept()
            return
        elif self._is_resizing and self._resize_start_geom is not None and self._resize_start_global is not None:
            diff = global_pos - self._resize_start_global
            geom = self._resize_start_geom
            new_x = geom.x()
            new_y = geom.y()
            new_w = geom.width()
            new_h = geom.height()

            if self._resize_edge & self.EDGE_LEFT:
                new_w = max(self.minimumWidth(), geom.width() - diff.x())
                new_x = geom.right() - new_w
            elif self._resize_edge & self.EDGE_RIGHT:
                new_w = max(self.minimumWidth(), geom.width() + diff.x())

            if self._resize_edge & self.EDGE_TOP:
                new_h = max(self.minimumHeight(), geom.height() - diff.y())
                new_y = geom.bottom() - new_h
            elif self._resize_edge & self.EDGE_BOTTOM:
                new_h = max(self.minimumHeight(), geom.height() + diff.y())

            self.setGeometry(new_x, new_y, new_w, new_h)
            event.accept()
            return
        else:
            edge = self._detect_edge(pos)
            self._update_cursor_for_edge(edge)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._is_dragging = False
        self._is_resizing = False
        self.unsetCursor()
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            if pos.y() <= 50:
                self.toggle_maximize()
                event.accept()
                return
        super().mouseDoubleClickEvent(event)

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
            self.mode_selector.btn_standard.setChecked(True)
            self.stack.setCurrentIndex(0)
            self.display_card.show()
            self.display_card.set_mode_badge("STANDARD", show_angle=False)
            self._update_display_from_active_engine()
            self.resize_for_mode(500, 730)

        elif mode == MODE_SCIENTIFIC:
            self.mode_selector.btn_scientific.setChecked(True)
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
            self.mode_selector.btn_business.setChecked(True)
            self.stack.setCurrentIndex(2)
            self.display_card.hide()  # Business view has dedicated custom result cards
            self.resize_for_mode(680, 780)

    def resize_for_mode(self, target_width: int, target_height: int):
        # In fullscreen or maximized mode, window dimensions are controlled by the screen
        if self.isMaximized() or self.isFullScreen():
            return

        screen = QApplication.primaryScreen()
        avail = screen.availableGeometry() if screen else None
        max_w = avail.width() - 24 if avail else 1900
        max_h = avail.height() - 48 if avail else 1000

        if self.history_panel.isVisible():
            target_width += 340

        safe_w = min(target_width, max_w)
        safe_h = min(target_height, max_h)

        if self.width() < safe_w or self.height() < safe_h:
            self.resize(max(self.width(), safe_w), max(self.height(), safe_h))

    def _toggle_history(self):
        is_visible = not self.history_panel.isVisible()
        self.history_panel.setVisible(is_visible)
        self.mode_selector.set_history_active(is_visible)

        if is_visible:
            self.history_panel.refresh()

        # If window is maximized or in fullscreen, DO NOT resize the window!
        # The window occupies the display, and the history drawer seamlessly opens/closes in-place.
        if self.isMaximized() or self.isFullScreen():
            return

        screen = QApplication.primaryScreen()
        avail = screen.availableGeometry() if screen else None
        max_w = avail.width() - 24 if avail else 1900
        panel_w = 340

        if is_visible:
            target_w = self.width() + panel_w
            new_w = min(target_w, max_w)
            # If expanding would push the right edge off-screen, shift window left so history is 100% visible
            if screen and avail:
                if self.x() + new_w > avail.right() - 8:
                    new_x = max(avail.left() + 8, avail.right() - 8 - new_w)
                    self.move(new_x, self.y())
            self.resize(new_w, self.height())
        else:
            new_w = max(self.minimumWidth(), self.width() - panel_w)
            self.resize(new_w, self.height())

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
        self.scientific_engine.percentage()
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

        # F11 Fullscreen toggle
        if key == Qt.Key.Key_F11:
            self.toggle_fullscreen()
            return

        # Escape closes fullscreen or history drawer
        if key == Qt.Key.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
                return
            if self.history_panel.isVisible():
                self._toggle_history()
                return

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

        # Percentage
        if text == "%":
            if self.current_mode == MODE_STANDARD:
                self._on_standard_percentage()
            elif self.current_mode == MODE_SCIENTIFIC:
                self._on_scientific_percentage()
            return

        # Operators
        if text in ("+", "-", "*", "/", "^"):
            op_map = {"+": "+", "-": "−", "*": "×", "/": "÷", "^": "^"}
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
