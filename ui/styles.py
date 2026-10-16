"""Luxury Minimalist Optical Glass stylesheet (QSS) inspired by Apple & high-end Swiss horology.

Design Principles:
- Monochromatic serenity: Smoked optical sapphire crystal with subtle refractive depth
- Exquisite minimalism: Razor-thin 1px hairlines, zero visual clutter, no garish toy colors
- Unified iconic amber crystal accent for operators & equals
- Floating emissive typography: Ultra-light, perfectly balanced figures (300 weight)
- Pure translucent body: True desktop and background application visibility
"""

def get_glass_theme(opacity_level: float = 0.40) -> str:
    """Generate luxury minimalist optical glass QSS with customizable background translucency.
    
    Args:
        opacity_level: Base glass opacity between 0.20 (ultra clear) and 0.65 (deep smoked glass).
    """
    op_top = max(0.15, opacity_level * 0.85)
    op_mid = max(0.22, opacity_level * 0.95)
    op_bot = min(0.75, opacity_level * 1.15)

    return f"""
/* ==========================================================================
   GLOBAL APP & LUXURY OPTICAL GLASS SLAB
   ========================================================================== */
QMainWindow {{
    background: transparent;
}}

QWidget#CentralWidget {{
    background: transparent;
}}

/* The Master Optical Glass Slab */
QFrame#GlassWindowFrame {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0.00 rgba(28, 32, 42, {op_top:.2f}),
        stop: 0.45 rgba(18, 21, 29, {op_mid:.2f}),
        stop: 1.00 rgba(12, 15, 22, {op_bot:.2f})
    );
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-top: 1px solid rgba(255, 255, 255, 0.28);
    border-radius: 26px;
}}

QToolTip {{
    background-color: rgba(22, 25, 34, 0.94);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 400;
}}

/* ==========================================================================
   MINIMALIST GLASS TITLE BAR & TRAFFIC LIGHTS
   ========================================================================== */
QFrame#GlassTitleBar {{
    background: transparent;
    border: none;
    padding: 0px 4px;
}}

/* Apple Minimalist Traffic Light Buttons */
QPushButton.traffic-close {{
    background-color: #FF5F56;
    border: none;
    border-radius: 6px;
    min-width: 12px;
    max-width: 12px;
    min-height: 12px;
    max-height: 12px;
    font-size: 8px;
    font-weight: 700;
    color: transparent;
}}

QPushButton.traffic-close:hover {{
    color: #4A0000;
}}

QPushButton.traffic-min {{
    background-color: #FFBD2E;
    border: none;
    border-radius: 6px;
    min-width: 12px;
    max-width: 12px;
    min-height: 12px;
    max-height: 12px;
    font-size: 8px;
    font-weight: 700;
    color: transparent;
}}

QPushButton.traffic-min:hover {{
    color: #4A3300;
}}

QPushButton.traffic-max {{
    background-color: #27C93F;
    border: none;
    border-radius: 6px;
    min-width: 12px;
    max-width: 12px;
    min-height: 12px;
    max-height: 12px;
    font-size: 8px;
    font-weight: 700;
    color: transparent;
}}

QPushButton.traffic-max:hover {{
    color: #003810;
}}

/* Discreet Luxury Title */
QLabel#GlassTitleLabel {{
    color: rgba(255, 255, 255, 0.40);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
}}

/* Minimalist Header Pills (Pin, Opacity) */
QPushButton.header-pill-btn {{
    background-color: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-top: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 8px;
    font-size: 11px;
    font-weight: 500;
    padding: 3px 10px;
    min-height: 18px;
}}

QPushButton.header-pill-btn:hover {{
    background-color: rgba(255, 255, 255, 0.12);
    color: #FFFFFF;
    border-top: 1px solid rgba(255, 255, 255, 0.35);
}}

QPushButton.header-pill-btn:checked {{
    background-color: rgba(255, 255, 255, 0.20);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.30);
}}

/* ==========================================================================
   SEGMENTED MODE SELECTOR (FLOATING CAPSULE)
   ========================================================================== */
QFrame#TopBarFrame {{
    background: transparent;
    border: none;
    padding: 0px;
}}

QFrame#SegmentedControl {{
    background-color: rgba(0, 0, 0, 0.22);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 3px;
}}

QPushButton.mode-pill {{
    background-color: transparent;
    color: rgba(255, 255, 255, 0.50);
    border: none;
    border-radius: 9px;
    font-size: 12px;
    font-weight: 500;
    padding: 6px 16px;
    min-height: 18px;
}}

QPushButton.mode-pill:hover {{
    color: rgba(255, 255, 255, 0.85);
    background-color: rgba(255, 255, 255, 0.05);
}}

QPushButton.mode-pill:checked {{
    background-color: rgba(255, 255, 255, 0.14);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-top: 1px solid rgba(255, 255, 255, 0.32);
    font-weight: 600;
}}

QPushButton.top-icon-btn {{
    background-color: rgba(255, 255, 255, 0.06);
    color: rgba(255, 255, 255, 0.70);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-top: 1px solid rgba(255, 255, 255, 0.20);
    border-radius: 11px;
    font-size: 12px;
    font-weight: 500;
    padding: 6px 14px;
    min-height: 20px;
}}

QPushButton.top-icon-btn:hover {{
    background-color: rgba(255, 255, 255, 0.14);
    color: #FFFFFF;
    border-top: 1px solid rgba(255, 255, 255, 0.40);
}}

QPushButton.top-icon-btn:checked {{
    background-color: rgba(255, 159, 10, 0.25);
    color: #FFB340;
    border: 1px solid rgba(255, 159, 10, 0.45);
}}

/* ==========================================================================
   DISPLAY CARD (SEAMLESS TRANSLUCENT HUD)
   ========================================================================== */
QFrame#DisplayCard {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-top: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 18px;
    padding: 12px 18px;
}}

QLabel#ExpressionLabel {{
    color: rgba(255, 255, 255, 0.45);
    font-size: 15px;
    font-weight: 400;
    letter-spacing: 0.5px;
}}

QLabel#ResultLabel {{
    color: #FFFFFF;
    font-size: 52px;
    font-weight: 300;
    letter-spacing: -0.5px;
}}

QLabel.badge-label {{
    background-color: rgba(255, 159, 10, 0.18);
    color: #FFB340;
    border: 1px solid rgba(255, 159, 10, 0.30);
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 10px;
    font-weight: 600;
}}

QLabel.badge-label-info {{
    background-color: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.70);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 10px;
    font-weight: 600;
}}

/* ==========================================================================
   LUXURY CRYSTAL KEYPAD BUTTONS
   ========================================================================== */
QPushButton.calc-btn {{
    border-radius: 18px;
    font-size: 20px;
    min-height: 38px;
    min-width: 38px;
    outline: none;
}}

/* 1. Numbers (0-9, .) - Pure Smoked Optical Sapphire */
QPushButton.btn-number {{
    background: rgba(255, 255, 255, 0.06);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-top: 1px solid rgba(255, 255, 255, 0.22);
    font-weight: 300;
}}

QPushButton.btn-number:hover {{
    background: rgba(255, 255, 255, 0.14);
    border-top: 1px solid rgba(255, 255, 255, 0.40);
}}

QPushButton.btn-number:pressed {{
    background: rgba(255, 255, 255, 0.03);
}}

/* 2. Utility Keys (AC, ±, %, ⌫) - Platinum Frosted Crystal */
QPushButton.btn-util {{
    background: rgba(255, 255, 255, 0.13);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-top: 1px solid rgba(255, 255, 255, 0.30);
    font-size: 18px;
    font-weight: 400;
}}

QPushButton.btn-util:hover {{
    background: rgba(255, 255, 255, 0.22);
    border-top: 1px solid rgba(255, 255, 255, 0.50);
}}

QPushButton.btn-util:pressed {{
    background: rgba(255, 255, 255, 0.07);
}}

/* 3. Micro-Pills for Memory Keys (MC, MR, M+, M-, MS) */
QPushButton.btn-memory {{
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.50);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 9px;
    font-size: 11px;
    font-weight: 500;
    min-height: 28px;
}}

QPushButton.btn-memory:hover {{
    background: rgba(255, 255, 255, 0.10);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.14);
}}

QPushButton.btn-memory:pressed {{
    background: rgba(255, 255, 255, 0.02);
}}

/* 4. Operators (+, −, ×, ÷) & Equals (=) - Unified Iconic Amber Glass */
QPushButton.btn-operator, QPushButton.btn-equals {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0.0 rgba(255, 168, 25, 0.92),
        stop: 1.0 rgba(245, 142, 0, 0.90)
    );
    color: #FFFFFF;
    border: 1px solid rgba(255, 200, 100, 0.20);
    border-top: 1px solid rgba(255, 255, 255, 0.45);
    font-size: 24px;
    font-weight: 400;
}}

QPushButton.btn-operator:hover, QPushButton.btn-equals:hover {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0.0 rgba(255, 185, 50, 0.98),
        stop: 1.0 rgba(255, 155, 10, 0.98)
    );
    border-top: 1px solid rgba(255, 255, 255, 0.70);
}}

QPushButton.btn-operator:pressed, QPushButton.btn-equals:pressed {{
    background-color: rgba(215, 120, 0, 0.95);
}}

/* 5. Scientific Keys - Smoked Quartz Glass */
QPushButton.btn-scientific {{
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.80);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-top: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 12px;
    font-size: 12px;
    font-weight: 400;
    min-height: 32px;
}}

QPushButton.btn-scientific:hover {{
    background: rgba(255, 255, 255, 0.12);
    color: #FFFFFF;
    border-top: 1px solid rgba(255, 255, 255, 0.30);
}}

QPushButton.btn-scientific:pressed {{
    background: rgba(255, 255, 255, 0.02);
}}

/* ==========================================================================
   BUSINESS & FINANCIAL VIEW (MINIMALIST TRANSLUCENT)
   ========================================================================== */
QFrame#BusinessCard {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-top: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 16px;
    padding: 16px;
}}

QTabWidget::pane {{
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-top: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 16px;
    background: rgba(14, 18, 26, 0.35);
    padding: 12px;
}}

QTabBar::tab {{
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.60);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    padding: 8px 14px;
    margin-right: 6px;
    margin-bottom: 6px;
    font-size: 12px;
    font-weight: 500;
}}

QTabBar::tab:hover {{
    background: rgba(255, 255, 255, 0.12);
    color: #FFFFFF;
}}

QTabBar::tab:selected {{
    background: rgba(255, 159, 10, 0.25);
    color: #FFB340;
    border: 1px solid rgba(255, 159, 10, 0.40);
    border-top: 1px solid rgba(255, 200, 100, 0.65);
}}

QLineEdit.business-input {{
    background: rgba(0, 0, 0, 0.25);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-top: 1px solid rgba(0, 0, 0, 0.35);
    border-bottom: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 15px;
    font-weight: 400;
    selection-background-color: #FF9F0A;
}}

QLineEdit.business-input:focus {{
    border: 1.5px solid #FF9F0A;
    background: rgba(0, 0, 0, 0.35);
}}

QComboBox.business-combo {{
    background: rgba(255, 255, 255, 0.06);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-top: 1px solid rgba(255, 255, 255, 0.22);
    border-radius: 10px;
    padding: 7px 12px;
    font-size: 13px;
    font-weight: 400;
}}

QComboBox.business-combo::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox QAbstractItemView {{
    background-color: rgba(22, 26, 36, 0.96);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 8px;
    selection-background-color: #FF9F0A;
}}

QPushButton.btn-action-primary {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 rgba(255, 168, 25, 0.90),
        stop: 1 rgba(240, 138, 0, 0.90)
    );
    color: #FFFFFF;
    border: 1px solid rgba(255, 200, 100, 0.35);
    border-top: 1px solid rgba(255, 255, 255, 0.50);
    border-radius: 11px;
    font-size: 14px;
    font-weight: 600;
    padding: 9px 18px;
    min-height: 22px;
}}

QPushButton.btn-action-primary:hover {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 rgba(255, 180, 45, 0.98),
        stop: 1 rgba(255, 150, 10, 0.98)
    );
}}

QPushButton.btn-action-secondary {{
    background-color: rgba(255, 255, 255, 0.06);
    color: rgba(255, 255, 255, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-top: 1px solid rgba(255, 255, 255, 0.22);
    border-radius: 10px;
    font-size: 12px;
    font-weight: 500;
    padding: 6px 12px;
}}

QPushButton.btn-action-secondary:hover {{
    background-color: rgba(255, 255, 255, 0.14);
    color: #FFFFFF;
}}

QFrame#BusinessResultFrame {{
    background: rgba(0, 0, 0, 0.30);
    border: 1px solid rgba(255, 159, 10, 0.25);
    border-top: 1px solid rgba(255, 180, 70, 0.40);
    border-radius: 14px;
    padding: 12px 16px;
}}

QLabel.result-value-highlight {{
    color: #FFB340;
    font-size: 24px;
    font-weight: 600;
}}

/* ==========================================================================
   HISTORY DRAWER PANEL
   ========================================================================== */
QFrame#HistoryPanel {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0.00 rgba(18, 22, 32, 0.65),
        stop: 1.00 rgba(12, 15, 22, 0.80)
    );
    border-left: 1px solid rgba(255, 255, 255, 0.12);
    border-top: 1px solid rgba(255, 255, 255, 0.22);
    border-top-left-radius: 20px;
    border-bottom-left-radius: 20px;
    padding: 0px;
}}

QScrollArea {{
    border: none;
    background: transparent;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 5px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background: rgba(255, 255, 255, 0.18);
    min-height: 24px;
    border-radius: 2px;
}}

QScrollBar::handle:vertical:hover {{
    background: rgba(255, 255, 255, 0.35);
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QFrame.history-entry-card {{
    background-color: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-top: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 11px;
    padding: 8px 12px;
}}

QFrame.history-entry-card:hover {{
    background-color: rgba(255, 255, 255, 0.10);
    border: 1px solid rgba(255, 255, 255, 0.18);
}}
"""

GLASS_THEME_QSS = get_glass_theme(0.40)
