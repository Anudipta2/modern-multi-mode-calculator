# Modern Multi-Mode Calculator for Windows

A modern desktop calculator application built with **Python 3** and **PySide6 (Qt for Python)** featuring an **Apple-inspired dark glassmorphism aesthetic**, responsive touchscreen-friendly interface, physical keyboard support, and three comprehensive calculation modes:

1. **Standard Calculator** (Everyday arithmetic with operator precedence, parentheses, memory registers, repeated equals)
2. **Scientific Calculator** (Trigonometry, inverse, hyperbolic, logarithms, arbitrary powers, roots, constants $\pi, e, \phi$, factorials, permutations $nPr$, combinations $nCr$, angle modes DEG / RAD / GRAD)
3. **Business & Financial Calculator** (Indian GST with CGST/SGST/IGST breakdown, Profit & Loss, Discount, Loan & EMI with schedule preview, Simple & Compound Interest, Multi-Currency $\text{₹}, \$, \text{€}, \text{£}, \text{¥}$, and Percentage/Ratio tools)

---

## Key Features

- **Apple Glassmorphism UI**: Deep charcoal translucent backgrounds, frosted acrylic panels, subtle borders, glowing active button states, and modern typography (`SF Pro Display` / `Segoe UI Variable`).
- **Dynamic Display Scaling**: High-resolution result line automatically scales its font down as numbers or expressions lengthen, ensuring digits never clip or overflow.
- **AST Safe Expression Parser**: Evaluates mathematical expressions using a restricted Abstract Syntax Tree (AST). Completely safe against code execution vulnerabilities (never uses unsafe unrestricted `eval()`).
- **High Financial Precision**: Financial calculations use Python's `Decimal` module with strict rounding (`ROUND_HALF_UP`) to prevent floating-point inaccuracies.
- **Indian GST Suite**: Specialized support for standard GST rates (0%, 5%, 12%, 18%, 28%, and custom rates) with both Add GST (exclusive) and Remove GST (inclusive) and automatic split into CGST + SGST (intra-state) or IGST (inter-state).
- **Persistent Calculation History**: Collapsible sliding history drawer with filtering, one-click result reuse, clipboard copying, and automatic disk persistence in JSON format.
- **Touchscreen & Keyboard Ready**: Generous button hit-targets ($\ge 52\text{px}$) with visual pressed states, plus full physical keyboard mappings.

---

## Project Structure

```text
ModernCalculator/
│
├── main.py                        # Application entry point & Qt initialization
│
├── core/
│   ├── constants.py               # Mathematical constants (π, e, φ), modes, currencies
│   ├── formatter.py               # Number formatting, commas, Indian grouping, currency
│   ├── expression_parser.py       # Safe AST-based expression engine (no eval)
│   └── history.py                 # Persistent calculation history with JSON storage
│
├── calculators/
│   ├── standard.py                # Standard calculator state engine & repeated equals
│   ├── scientific.py              # Scientific calculator engine with angle modes
│   └── business.py                # Financial controller with currency formatting
│
├── finance/
│   ├── gst.py                     # GST calculator (Add/Remove, CGST, SGST, IGST)
│   ├── emi.py                     # Reducing-balance Loan & EMI calculator
│   ├── interest.py                # Simple and Compound Interest (5 frequencies)
│   ├── profit_loss.py             # Cost Price, Selling Price, Profit/Loss %
│   ├── discount.py                # Marked Price, Discount %, Savings
│   └── ratios.py                  # % of number, % change, ratio simplification
│
├── ui/
│   ├── styles.py                  # Dark glassmorphic QSS stylesheet
│   ├── calculator_display.py      # Glass display with dynamic auto-scaling text
│   ├── mode_selector.py           # Apple-style segmented mode control & history button
│   ├── keypad.py                  # Standard and Scientific touch-friendly keypads
│   ├── business_view.py           # Financial dashboard with 6 specialized tabs
│   ├── history_panel.py           # Collapsible history drawer with reuse/copy
│   └── main_window.py             # Main window coordinating UI, state & shortcuts
│
├── tests/
│   ├── test_calculator.py         # Unit tests for math, security, GST, EMI, interest
│   └── test_ui.py                 # PySide6 UI integration and mode switching tests
│
├── requirements.txt               # Dependencies list
└── README.md                      # Documentation & instructions
```

---

## Installation & Running

### Option 1: Quick Run with `uv` (Recommended)

If you have `uv` installed:

```powershell
cd c:\Users\anudi\OneDrive\Documents\ModernCalculator
uv run main.py
```

Or from the root Documents directory:

```powershell
python calculator.py
```

### Option 2: Standard Python Virtual Environment

1. Create and activate a virtual environment:
   ```powershell
   cd c:\Users\anudi\OneDrive\Documents\ModernCalculator
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Launch the calculator:
   ```powershell
   python main.py
   ```

---

## Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `0` – `9` | Enter numbers |
| `.` | Enter decimal point |
| `+`, `-`, `*`, `/` | Arithmetic operators ($+$, $-$, $\times$, $\div$) |
| `%` | Percentage calculation |
| `^` | Exponentiation / Power |
| `(` and `)` | Parentheses |
| `Enter` or `=` | Calculate / Evaluate result |
| `Backspace` | Delete last digit |
| `Escape` | All Clear (`AC`) |
| `C` or `c` | Clear current entry |
| `Ctrl + 1` | Switch to **Standard Mode** |
| `Ctrl + 2` | Switch to **Scientific Mode** |
| `Ctrl + 3` | Switch to **Business Mode** |
| `Ctrl + H` | Toggle **History Drawer** |
| `Ctrl + C` | Copy current display to clipboard |
| `Ctrl + V` | Paste number or expression from clipboard |

---

## Running the Automated Test Suite

The project includes unit and UI integration tests verifying math accuracy, operator precedence, AST security against code injection, financial formulas, and PySide6 UI components.

Run all tests via `pytest`:

```powershell
cd c:\Users\anudi\OneDrive\Documents\ModernCalculator
.venv\Scripts\python.exe -m pytest tests -v
```

Output:
```text
============================= 21 passed in 2.18s ==============================
```

---

## Windows Application Installation

You can install Modern Multi-Mode Calculator as a full native Windows desktop application with Start Menu integration, Desktop shortcut, and Windows Settings entry.

### Method 1: One-Click Installer (Recommended)

1. Navigate to the [`installer/`](file:///c:/Users/anudi/OneDrive/Documents/ModernCalculator/installer) folder:
   - Double-click [`install.bat`](file:///c:/Users/anudi/OneDrive/Documents/ModernCalculator/installer/install.bat)
   - Or run from PowerShell:
     ```powershell
     powershell -ExecutionPolicy Bypass -File .\installer\install.ps1
     ```

2. **What the installer does automatically**:
   - Copies the compiled executable and high-resolution icons to `%LOCALAPPDATA%\Programs\ModernCalculator\` (no Admin privileges required).
   - Creates a **Windows Start Menu shortcut** (`Modern Multi-Mode Calculator`).
   - Creates a **Desktop shortcut**.
   - Registers the application in Windows **Settings > Apps > Installed apps** (Add or Remove Programs) with version info, publisher, and size.
   - Installs a dedicated uninstaller.

### Method 2: Standalone Portable Executable

If you do not want to install shortcuts or registry entries, you can run or share the portable `.exe` directly:
```text
c:\Users\anudi\OneDrive\Documents\ModernCalculator\dist\ModernCalculator.exe
```
This single executable has all Qt libraries, Python runtime, and assets embedded into it and runs on any modern Windows 10/11 system without requiring Python.

### Method 3: Inno Setup Wizard Installer

If you prefer building a traditional multi-step Windows Setup Wizard (`ModernCalculatorSetup.exe`):
1. Install [Inno Setup](https://jrsoftware.org/isdl.php).
2. Open [`installer/ModernCalculatorSetup.iss`](file:///c:/Users/anudi/OneDrive/Documents/ModernCalculator/installer/ModernCalculatorSetup.iss) in Inno Setup Compiler.
3. Click **Build > Compile**. The installer will be generated in `dist/setup/ModernCalculatorSetup.exe`.

---

## Uninstalling the Application

You can uninstall the application cleanly at any time through either:

1. **Windows Settings**:
   - Open **Windows Settings > Apps > Installed apps** (or "Add or Remove Programs").
   - Find **Modern Multi-Mode Calculator**.
   - Click **Uninstall**.

2. **Direct Script**:
   - Run [`uninstall.bat`](file:///c:/Users/anudi/OneDrive/Documents/ModernCalculator/installer/uninstall.bat) or `uninstall.ps1` from the installation directory.

