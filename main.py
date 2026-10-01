"""Entry point for the Modern Multi-Mode Calculator application."""

import sys
import os
import ctypes

# Handle PyInstaller _MEIPASS resource extraction directory
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPalette, QIcon

from ui.main_window import ModernCalculatorWindow


def main():
    # Set Windows Taskbar AppUserModelID so the icon appears correctly in the taskbar
    try:
        myappid = "Antigravity.ModernCalculator.App.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Modern Multi-Mode Calculator")
    app.setOrganizationName("Antigravity")

    # Set Window Icon
    icon_path = os.path.join(BASE_DIR, "assets", "icon.ico")
    if not os.path.exists(icon_path):
        icon_path = os.path.join(BASE_DIR, "assets", "icon.png")
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)

    # Set modern system-preferred font
    font = QFont()
    font.setFamilies([
        "SF Pro Display",
        "Segoe UI Variable Display",
        "Segoe UI",
        "Inter",
        "Helvetica Neue",
        "Arial",
    ])
    font.setPointSize(10)
    app.setFont(font)

    # Dark base palette to prevent bright flashing during widget instantiation
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#121316"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#F5F5F7"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#1A1C22"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#22252E"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#FFFFFF"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#252834"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#FFFFFF"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#FF9F0A"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#000000"))
    app.setPalette(palette)

    window = ModernCalculatorWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
