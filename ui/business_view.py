"""Dedicated Business and Financial Calculator view component."""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QRadioButton,
    QButtonGroup,
    QTabWidget,
    QFrame,
    QScrollArea,
    QApplication,
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QCursor, QFont
from calculators.business import BusinessCalculatorEngine
from core.constants import CURRENCIES, GST_RATES, COMPOUND_FREQUENCIES


class BusinessView(QWidget):
    """Modern Apple-styled business & financial dashboard with multi-currency support."""

    calculation_completed = Signal(str, str)  # expression, result

    def __init__(self, engine: BusinessCalculatorEngine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)

        # --- Top Currency Selector Bar ---
        curr_frame = QFrame()
        curr_frame.setObjectName("SegmentedControl")
        curr_layout = QHBoxLayout(curr_frame)
        curr_layout.setContentsMargins(4, 4, 4, 4)
        curr_layout.setSpacing(6)

        curr_label = QLabel("Currency:")
        curr_label.setStyleSheet("color: #989BA5; font-weight: 600; font-size: 13px; margin-left: 6px;")
        curr_layout.addWidget(curr_label)

        self.curr_btn_group = QButtonGroup(self)
        self.curr_btn_group.setExclusive(True)

        for i, (code, info) in enumerate(CURRENCIES.items()):
            btn = QPushButton(f"{info['symbol']} {code}")
            btn.setProperty("class", "mode-pill")
            btn.setCheckable(True)
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            if code == self.engine.currency_code:
                btn.setChecked(True)
            btn.clicked.connect(lambda _, c=code: self._on_currency_changed(c))
            self.curr_btn_group.addButton(btn, i)
            curr_layout.addWidget(btn)

        curr_layout.addStretch()
        main_layout.addWidget(curr_frame)

        # --- Tabbed Financial Tools ---
        self.tabs = QTabWidget()
        self.tabs.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tabs.addTab(self._create_gst_tab(), "💰 GST / Tax")
        self.tabs.addTab(self._create_profit_loss_tab(), "📈 Profit & Loss")
        self.tabs.addTab(self._create_discount_tab(), "🏷️ Discount")
        self.tabs.addTab(self._create_emi_tab(), "🏦 Loan & EMI")
        self.tabs.addTab(self._create_interest_tab(), "📊 Interest (SI/CI)")
        self.tabs.addTab(self._create_ratios_tab(), "🔢 % & Ratios")

        main_layout.addWidget(self.tabs)

    def _on_currency_changed(self, code: str):
        self.engine.set_currency(code)
        # Recalculate active tab
        self._calculate_gst()
        self._calculate_profit_loss()
        self._calculate_discount()
        self._calculate_emi()
        self._calculate_interest()

    # =========================================================================
    # TAB 1: GST / TAX CALCULATOR
    # =========================================================================
    def _create_gst_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)

        # Inputs
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(QLabel("Amount:"), 0, 0)
        self.gst_amount_input = QLineEdit("1000")
        self.gst_amount_input.setProperty("class", "business-input")
        self.gst_amount_input.textChanged.connect(self._calculate_gst)
        grid.addWidget(self.gst_amount_input, 0, 1)

        # Add / Remove GST Radio Buttons
        grid.addWidget(QLabel("GST Mode:"), 1, 0)
        mode_box = QHBoxLayout()
        self.gst_mode_add = QRadioButton("Add GST (Exclusive)")
        self.gst_mode_remove = QRadioButton("Remove GST (Inclusive)")
        self.gst_mode_add.setChecked(True)
        self.gst_mode_add.toggled.connect(self._calculate_gst)
        self.gst_mode_remove.toggled.connect(self._calculate_gst)
        mode_box.addWidget(self.gst_mode_add)
        mode_box.addWidget(self.gst_mode_remove)
        grid.addLayout(mode_box, 1, 1)

        # GST Rate Selector Pills
        grid.addWidget(QLabel("GST Rate:"), 2, 0)
        rate_layout = QHBoxLayout()
        rate_layout.setSpacing(6)
        self.gst_rate_group = QButtonGroup(self)
        self.gst_rate_buttons = []
        for rate in GST_RATES:
            rbtn = QPushButton(f"{rate}%")
            rbtn.setProperty("class", "mode-pill")
            rbtn.setCheckable(True)
            if rate == 18:
                rbtn.setChecked(True)
            rbtn.clicked.connect(lambda _, r=rate: self._set_gst_rate(r))
            self.gst_rate_group.addButton(rbtn)
            self.gst_rate_buttons.append(rbtn)
            rate_layout.addWidget(rbtn)

        # Custom rate input
        self.gst_custom_rate = QLineEdit("18")
        self.gst_custom_rate.setPlaceholderText("Custom %")
        self.gst_custom_rate.setMaximumWidth(90)
        self.gst_custom_rate.setProperty("class", "business-input")
        self.gst_custom_rate.textChanged.connect(self._calculate_gst)
        rate_layout.addWidget(self.gst_custom_rate)
        grid.addLayout(rate_layout, 2, 1)

        # Transaction type: Intra-state vs Inter-state
        grid.addWidget(QLabel("Supply Type:"), 3, 0)
        trans_box = QHBoxLayout()
        self.gst_intra_state = QRadioButton("Intra-state (CGST + SGST)")
        self.gst_inter_state = QRadioButton("Inter-state (IGST)")
        self.gst_intra_state.setChecked(True)
        self.gst_intra_state.toggled.connect(self._calculate_gst)
        self.gst_inter_state.toggled.connect(self._calculate_gst)
        trans_box.addWidget(self.gst_intra_state)
        trans_box.addWidget(self.gst_inter_state)
        grid.addLayout(trans_box, 3, 1)

        layout.addLayout(grid)

        # Results Frame
        self.gst_result_frame = QFrame()
        self.gst_result_frame.setObjectName("BusinessResultFrame")
        res_layout = QVBoxLayout(self.gst_result_frame)
        res_layout.setSpacing(6)

        self.gst_final_label = QLabel("Total: ₹1,180.00")
        self.gst_final_label.setProperty("class", "result-value-highlight")
        res_layout.addWidget(self.gst_final_label)

        self.gst_details_label = QLabel("Base Price: ₹1,000.00 | GST (18%): ₹180.00\nCGST (9%): ₹90.00 | SGST (9%): ₹90.00")
        self.gst_details_label.setStyleSheet("color: #D1D5DB; font-size: 13px; line-height: 1.4;")
        res_layout.addWidget(self.gst_details_label)

        # Action Buttons
        btn_box = QHBoxLayout()
        btn_copy = QPushButton("📋 Copy Result")
        btn_copy.setProperty("class", "btn-action-secondary")
        btn_copy.clicked.connect(lambda: self._copy_text(self.gst_final_label.text(), btn_copy))

        btn_hist = QPushButton("💾 Log to History")
        btn_hist.setProperty("class", "btn-action-secondary")
        btn_hist.clicked.connect(self._log_gst_to_history)

        btn_box.addWidget(btn_copy)
        btn_box.addWidget(btn_hist)
        btn_box.addStretch()
        res_layout.addLayout(btn_box)

        layout.addWidget(self.gst_result_frame)
        layout.addStretch()

        self._calculate_gst()
        return widget

    def _set_gst_rate(self, rate: int):
        self.gst_custom_rate.setText(str(rate))
        self._calculate_gst()

    def _calculate_gst(self):
        try:
            amt = self.gst_amount_input.text()
            rate = self.gst_custom_rate.text()
            is_inter = self.gst_inter_state.isChecked()

            if self.gst_mode_add.isChecked():
                res = self.engine.compute_gst_add(amt, rate, is_inter)
                self.gst_final_label.setText(f"Final Total: {res['fmt_final_price']}")
                if is_inter:
                    details = f"Base Price: {res['fmt_base_price']} | Total GST ({res['gst_rate']}%): {res['fmt_gst_amount']}\nIGST: {res['fmt_igst']}"
                else:
                    details = f"Base Price: {res['fmt_base_price']} | Total GST ({res['gst_rate']}%): {res['fmt_gst_amount']}\nCGST ({res['gst_rate']/2}%): {res['fmt_cgst']} | SGST ({res['gst_rate']/2}%): {res['fmt_sgst']}"
            else:
                res = self.engine.compute_gst_remove(amt, rate, is_inter)
                self.gst_final_label.setText(f"Net Base Price: {res['fmt_base_price']}")
                if is_inter:
                    details = f"Gross Price: {res['fmt_final_price']} | GST Deducted ({res['gst_rate']}%): {res['fmt_gst_amount']}\nIGST: {res['fmt_igst']}"
                else:
                    details = f"Gross Price: {res['fmt_final_price']} | GST Deducted ({res['gst_rate']}%): {res['fmt_gst_amount']}\nCGST ({res['gst_rate']/2}%): {res['fmt_cgst']} | SGST ({res['gst_rate']/2}%): {res['fmt_sgst']}"

            self.gst_details_label.setText(details)
        except Exception:
            self.gst_final_label.setText("Invalid Input")

    def _log_gst_to_history(self):
        expr = f"GST {self.gst_custom_rate.text()}% on {self.engine.currency_symbol}{self.gst_amount_input.text()}"
        res = self.gst_final_label.text()
        self.calculation_completed.emit(expr, res)

    # =========================================================================
    # TAB 2: PROFIT & LOSS CALCULATOR
    # =========================================================================
    def _create_profit_loss_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(QLabel("Cost Price (CP):"), 0, 0)
        self.pl_cp_input = QLineEdit("1000")
        self.pl_cp_input.setProperty("class", "business-input")
        self.pl_cp_input.textChanged.connect(self._calculate_profit_loss)
        grid.addWidget(self.pl_cp_input, 0, 1)

        grid.addWidget(QLabel("Selling Price (SP):"), 1, 0)
        self.pl_sp_input = QLineEdit("1250")
        self.pl_sp_input.setProperty("class", "business-input")
        self.pl_sp_input.textChanged.connect(self._calculate_profit_loss)
        grid.addWidget(self.pl_sp_input, 1, 1)

        layout.addLayout(grid)

        # Results Frame
        res_frame = QFrame()
        res_frame.setObjectName("BusinessResultFrame")
        res_layout = QVBoxLayout(res_frame)
        res_layout.setSpacing(6)

        self.pl_result_label = QLabel("PROFIT: ₹250.00 (+25%)")
        self.pl_result_label.setProperty("class", "result-value-highlight")
        res_layout.addWidget(self.pl_result_label)

        self.pl_details_label = QLabel("Cost: ₹1,000.00 | Selling: ₹1,250.00")
        self.pl_details_label.setStyleSheet("color: #D1D5DB; font-size: 13px;")
        res_layout.addWidget(self.pl_details_label)

        btn_box = QHBoxLayout()
        btn_copy = QPushButton("📋 Copy Result")
        btn_copy.setProperty("class", "btn-action-secondary")
        btn_copy.clicked.connect(lambda: self._copy_text(self.pl_result_label.text(), btn_copy))

        btn_hist = QPushButton("💾 Log to History")
        btn_hist.setProperty("class", "btn-action-secondary")
        btn_hist.clicked.connect(self._log_pl_to_history)

        btn_box.addWidget(btn_copy)
        btn_box.addWidget(btn_hist)
        btn_box.addStretch()
        res_layout.addLayout(btn_box)

        layout.addWidget(res_frame)
        layout.addStretch()

        self._calculate_profit_loss()
        return widget

    def _calculate_profit_loss(self):
        try:
            cp = self.pl_cp_input.text()
            sp = self.pl_sp_input.text()
            res = self.engine.compute_profit_loss(cp, sp)

            status = res["status"].upper()
            if status == "PROFIT":
                self.pl_result_label.setStyleSheet("color: #30D158; font-size: 24px; font-weight: 700;")
                self.pl_result_label.setText(f"PROFIT: {res['fmt_amount']} (+{res['fmt_percentage']})")
            elif status == "LOSS":
                self.pl_result_label.setStyleSheet("color: #FF453A; font-size: 24px; font-weight: 700;")
                self.pl_result_label.setText(f"LOSS: {res['fmt_amount']} (-{res['fmt_percentage']})")
            else:
                self.pl_result_label.setStyleSheet("color: #989BA5; font-size: 24px; font-weight: 700;")
                self.pl_result_label.setText("BREAK EVEN (0% Profit/Loss)")

            self.pl_details_label.setText(f"Cost Price: {res['fmt_cost_price']} | Selling Price: {res['fmt_selling_price']}")
        except Exception:
            self.pl_result_label.setText("Invalid Input")

    def _log_pl_to_history(self):
        expr = f"P&L (CP: {self.engine.currency_symbol}{self.pl_cp_input.text()}, SP: {self.engine.currency_symbol}{self.pl_sp_input.text()})"
        res = self.pl_result_label.text()
        self.calculation_completed.emit(expr, res)

    # =========================================================================
    # TAB 3: DISCOUNT CALCULATOR
    # =========================================================================
    def _create_discount_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(QLabel("Marked Price (MRP):"), 0, 0)
        self.disc_mp_input = QLineEdit("2000")
        self.disc_mp_input.setProperty("class", "business-input")
        self.disc_mp_input.textChanged.connect(self._calculate_discount)
        grid.addWidget(self.disc_mp_input, 0, 1)

        grid.addWidget(QLabel("Discount (%):"), 1, 0)
        self.disc_rate_input = QLineEdit("15")
        self.disc_rate_input.setProperty("class", "business-input")
        self.disc_rate_input.textChanged.connect(self._calculate_discount)
        grid.addWidget(self.disc_rate_input, 1, 1)

        layout.addLayout(grid)

        res_frame = QFrame()
        res_frame.setObjectName("BusinessResultFrame")
        res_layout = QVBoxLayout(res_frame)
        res_layout.setSpacing(6)

        self.disc_final_label = QLabel("Final Price: ₹1,700.00")
        self.disc_final_label.setProperty("class", "result-value-highlight")
        res_layout.addWidget(self.disc_final_label)

        self.disc_details_label = QLabel("You Save: ₹300.00 (15%)")
        self.disc_details_label.setStyleSheet("color: #30D158; font-size: 14px; font-weight: 600;")
        res_layout.addWidget(self.disc_details_label)

        btn_box = QHBoxLayout()
        btn_copy = QPushButton("📋 Copy Result")
        btn_copy.setProperty("class", "btn-action-secondary")
        btn_copy.clicked.connect(lambda: self._copy_text(self.disc_final_label.text(), btn_copy))

        btn_hist = QPushButton("💾 Log to History")
        btn_hist.setProperty("class", "btn-action-secondary")
        btn_hist.clicked.connect(self._log_discount_to_history)

        btn_box.addWidget(btn_copy)
        btn_box.addWidget(btn_hist)
        btn_box.addStretch()
        res_layout.addLayout(btn_box)

        layout.addWidget(res_frame)
        layout.addStretch()

        self._calculate_discount()
        return widget

    def _calculate_discount(self):
        try:
            mp = self.disc_mp_input.text()
            dp = self.disc_rate_input.text()
            res = self.engine.compute_discount(mp, dp)
            self.disc_final_label.setText(f"Final Price: {res['fmt_final_price']}")
            self.disc_details_label.setText(f"You Save: {res['fmt_discount_amount']} ({res['fmt_discount_percent']})")
        except Exception:
            self.disc_final_label.setText("Invalid Input")

    def _log_discount_to_history(self):
        expr = f"Discount {self.disc_rate_input.text()}% on {self.engine.currency_symbol}{self.disc_mp_input.text()}"
        res = self.disc_final_label.text()
        self.calculation_completed.emit(expr, res)

    # =========================================================================
    # TAB 4: LOAN & EMI CALCULATOR
    # =========================================================================
    def _create_emi_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        grid = QGridLayout()
        grid.setSpacing(8)

        grid.addWidget(QLabel("Loan Amount:"), 0, 0)
        self.emi_principal_input = QLineEdit("100000")
        self.emi_principal_input.setProperty("class", "business-input")
        self.emi_principal_input.textChanged.connect(self._calculate_emi)
        grid.addWidget(self.emi_principal_input, 0, 1)

        grid.addWidget(QLabel("Annual Interest Rate (%):"), 1, 0)
        self.emi_rate_input = QLineEdit("10.5")
        self.emi_rate_input.setProperty("class", "business-input")
        self.emi_rate_input.textChanged.connect(self._calculate_emi)
        grid.addWidget(self.emi_rate_input, 1, 1)

        grid.addWidget(QLabel("Loan Tenure:"), 2, 0)
        tenure_box = QHBoxLayout()
        self.emi_tenure_input = QLineEdit("2")
        self.emi_tenure_input.setProperty("class", "business-input")
        self.emi_tenure_input.textChanged.connect(self._calculate_emi)

        self.emi_unit_combo = QComboBox()
        self.emi_unit_combo.addItems(["Years", "Months"])
        self.emi_unit_combo.setProperty("class", "business-combo")
        self.emi_unit_combo.currentIndexChanged.connect(self._calculate_emi)

        tenure_box.addWidget(self.emi_tenure_input)
        tenure_box.addWidget(self.emi_unit_combo)
        grid.addLayout(tenure_box, 2, 1)

        layout.addLayout(grid)

        # Results Frame
        res_frame = QFrame()
        res_frame.setObjectName("BusinessResultFrame")
        res_layout = QVBoxLayout(res_frame)
        res_layout.setSpacing(6)

        self.emi_monthly_label = QLabel("Monthly EMI: ₹4,637.60")
        self.emi_monthly_label.setProperty("class", "result-value-highlight")
        res_layout.addWidget(self.emi_monthly_label)

        self.emi_details_label = QLabel("Total Interest: ₹11,302.40 | Total Payable: ₹111,302.40")
        self.emi_details_label.setStyleSheet("color: #D1D5DB; font-size: 13px;")
        res_layout.addWidget(self.emi_details_label)

        btn_box = QHBoxLayout()
        btn_copy = QPushButton("📋 Copy EMI")
        btn_copy.setProperty("class", "btn-action-secondary")
        btn_copy.clicked.connect(lambda: self._copy_text(self.emi_monthly_label.text(), btn_copy))

        btn_hist = QPushButton("💾 Log to History")
        btn_hist.setProperty("class", "btn-action-secondary")
        btn_hist.clicked.connect(self._log_emi_to_history)

        btn_box.addWidget(btn_copy)
        btn_box.addWidget(btn_hist)
        btn_box.addStretch()
        res_layout.addLayout(btn_box)

        layout.addWidget(res_frame)
        layout.addStretch()

        self._calculate_emi()
        return widget

    def _calculate_emi(self):
        try:
            p = self.emi_principal_input.text()
            r = self.emi_rate_input.text()
            t = self.emi_tenure_input.text()
            unit = self.emi_unit_combo.currentText().lower()
            res = self.engine.compute_emi(p, r, t, unit)

            self.emi_monthly_label.setText(f"Monthly EMI: {res['fmt_monthly_emi']}")
            self.emi_details_label.setText(f"Total Interest: {res['fmt_total_interest']} | Total Payable: {res['fmt_total_payable']}")
        except Exception:
            self.emi_monthly_label.setText("Invalid Input")

    def _log_emi_to_history(self):
        expr = f"Loan EMI (P: {self.engine.currency_symbol}{self.emi_principal_input.text()}, Rate: {self.emi_rate_input.text()}%, Tenure: {self.emi_tenure_input.text()} {self.emi_unit_combo.currentText()})"
        res = self.emi_monthly_label.text()
        self.calculation_completed.emit(expr, res)

    # =========================================================================
    # TAB 5: SIMPLE & COMPOUND INTEREST
    # =========================================================================
    def _create_interest_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        grid = QGridLayout()
        grid.setSpacing(8)

        grid.addWidget(QLabel("Principal:"), 0, 0)
        self.intr_principal_input = QLineEdit("10000")
        self.intr_principal_input.setProperty("class", "business-input")
        self.intr_principal_input.textChanged.connect(self._calculate_interest)
        grid.addWidget(self.intr_principal_input, 0, 1)

        grid.addWidget(QLabel("Annual Rate (%):"), 1, 0)
        self.intr_rate_input = QLineEdit("7.5")
        self.intr_rate_input.setProperty("class", "business-input")
        self.intr_rate_input.textChanged.connect(self._calculate_interest)
        grid.addWidget(self.intr_rate_input, 1, 1)

        grid.addWidget(QLabel("Time:"), 2, 0)
        t_box = QHBoxLayout()
        self.intr_time_input = QLineEdit("3")
        self.intr_time_input.setProperty("class", "business-input")
        self.intr_time_input.textChanged.connect(self._calculate_interest)

        self.intr_time_unit_combo = QComboBox()
        self.intr_time_unit_combo.addItems(["Years", "Months", "Days"])
        self.intr_time_unit_combo.setProperty("class", "business-combo")
        self.intr_time_unit_combo.currentIndexChanged.connect(self._calculate_interest)

        t_box.addWidget(self.intr_time_input)
        t_box.addWidget(self.intr_time_unit_combo)
        grid.addLayout(t_box, 2, 1)

        # Simple vs Compound
        grid.addWidget(QLabel("Interest Type:"), 3, 0)
        type_box = QHBoxLayout()
        self.intr_type_simple = QRadioButton("Simple Interest")
        self.intr_type_compound = QRadioButton("Compound Interest")
        self.intr_type_compound.setChecked(True)
        self.intr_type_simple.toggled.connect(self._calculate_interest)
        self.intr_type_compound.toggled.connect(self._calculate_interest)
        type_box.addWidget(self.intr_type_compound)
        type_box.addWidget(self.intr_type_simple)
        grid.addLayout(type_box, 3, 1)

        # Compounding Frequency
        grid.addWidget(QLabel("Compounding:"), 4, 0)
        self.intr_freq_combo = QComboBox()
        self.intr_freq_combo.addItems(list(COMPOUND_FREQUENCIES.keys()))
        self.intr_freq_combo.setProperty("class", "business-combo")
        self.intr_freq_combo.currentIndexChanged.connect(self._calculate_interest)
        grid.addWidget(self.intr_freq_combo, 4, 1)

        layout.addLayout(grid)

        res_frame = QFrame()
        res_frame.setObjectName("BusinessResultFrame")
        res_layout = QVBoxLayout(res_frame)
        res_layout.setSpacing(6)

        self.intr_total_label = QLabel("Total Maturity: ₹12,497.16")
        self.intr_total_label.setProperty("class", "result-value-highlight")
        res_layout.addWidget(self.intr_total_label)

        self.intr_details_label = QLabel("Interest Earned: ₹2,497.16 | Principal: ₹10,000.00")
        self.intr_details_label.setStyleSheet("color: #D1D5DB; font-size: 13px;")
        res_layout.addWidget(self.intr_details_label)

        btn_box = QHBoxLayout()
        btn_copy = QPushButton("📋 Copy Total")
        btn_copy.setProperty("class", "btn-action-secondary")
        btn_copy.clicked.connect(lambda: self._copy_text(self.intr_total_label.text(), btn_copy))

        btn_hist = QPushButton("💾 Log to History")
        btn_hist.setProperty("class", "btn-action-secondary")
        btn_hist.clicked.connect(self._log_interest_to_history)

        btn_box.addWidget(btn_copy)
        btn_box.addWidget(btn_hist)
        btn_box.addStretch()
        res_layout.addLayout(btn_box)

        layout.addWidget(res_frame)
        layout.addStretch()

        self._calculate_interest()
        return widget

    def _calculate_interest(self):
        try:
            p = self.intr_principal_input.text()
            r = self.intr_rate_input.text()
            t = self.intr_time_input.text()
            unit = self.intr_time_unit_combo.currentText().lower()

            if self.intr_type_simple.isChecked():
                self.intr_freq_combo.setEnabled(False)
                res = self.engine.compute_simple_interest(p, r, t, unit)
                title = "Simple Interest"
            else:
                self.intr_freq_combo.setEnabled(True)
                freq = self.intr_freq_combo.currentText()
                # If months/days, convert to years for compound
                t_float = float(t)
                if unit == "months":
                    t_years = t_float / 12.0
                elif unit == "days":
                    t_years = t_float / 365.0
                else:
                    t_years = t_float
                res = self.engine.compute_compound_interest(p, r, t_years, freq)
                title = f"Compound Interest ({freq})"

            self.intr_total_label.setText(f"Maturity Value: {res['fmt_total_amount']}")
            self.intr_details_label.setText(f"Interest Earned: {res['fmt_interest']} ({title}) | Principal: {res['fmt_principal']}")
        except Exception:
            self.intr_total_label.setText("Invalid Input")

    def _log_interest_to_history(self):
        t_type = "Simple Interest" if self.intr_type_simple.isChecked() else f"Compound Interest ({self.intr_freq_combo.currentText()})"
        expr = f"{t_type} on {self.engine.currency_symbol}{self.intr_principal_input.text()} @ {self.intr_rate_input.text()}% for {self.intr_time_input.text()} {self.intr_time_unit_combo.currentText()}"
        res = self.intr_total_label.text()
        self.calculation_completed.emit(expr, res)

    # =========================================================================
    # TAB 6: PERCENTAGES & RATIOS
    # =========================================================================
    def _create_ratios_tab(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(14)

        # 1. Percentage of a number
        card1 = QFrame()
        card1.setProperty("class", "history-entry-card")
        c1_layout = QVBoxLayout(card1)
        c1_layout.addWidget(QLabel("<b>1. What is X% of Y?</b>"))
        row1 = QHBoxLayout()
        self.pct_x_input = QLineEdit("25")
        self.pct_x_input.setProperty("class", "business-input")
        self.pct_x_input.setPlaceholderText("X %")
        self.pct_y_input = QLineEdit("400")
        self.pct_y_input.setProperty("class", "business-input")
        self.pct_y_input.setPlaceholderText("Y (Total)")
        self.pct_res_label = QLabel("= 100")
        self.pct_res_label.setStyleSheet("color: #FF9F0A; font-weight: 700; font-size: 16px;")

        self.pct_x_input.textChanged.connect(self._recalc_pct_of)
        self.pct_y_input.textChanged.connect(self._recalc_pct_of)

        row1.addWidget(self.pct_x_input)
        row1.addWidget(QLabel("% of"))
        row1.addWidget(self.pct_y_input)
        row1.addWidget(self.pct_res_label)
        c1_layout.addLayout(row1)
        layout.addWidget(card1)

        # 2. Percentage Change
        card2 = QFrame()
        card2.setProperty("class", "history-entry-card")
        c2_layout = QVBoxLayout(card2)
        c2_layout.addWidget(QLabel("<b>2. Percentage Increase / Decrease (from Old to New)</b>"))
        row2 = QHBoxLayout()
        self.chg_old_input = QLineEdit("500")
        self.chg_old_input.setProperty("class", "business-input")
        self.chg_old_input.setPlaceholderText("Old Value")
        self.chg_new_input = QLineEdit("650")
        self.chg_new_input.setProperty("class", "business-input")
        self.chg_new_input.setPlaceholderText("New Value")
        self.chg_res_label = QLabel("= +30.00% increase")
        self.chg_res_label.setStyleSheet("color: #30D158; font-weight: 700; font-size: 16px;")

        self.chg_old_input.textChanged.connect(self._recalc_pct_change)
        self.chg_new_input.textChanged.connect(self._recalc_pct_change)

        row2.addWidget(self.chg_old_input)
        row2.addWidget(QLabel("→"))
        row2.addWidget(self.chg_new_input)
        row2.addWidget(self.chg_res_label)
        c2_layout.addLayout(row2)
        layout.addWidget(card2)

        # 3. Ratio Simplifier
        card3 = QFrame()
        card3.setProperty("class", "history-entry-card")
        c3_layout = QVBoxLayout(card3)
        c3_layout.addWidget(QLabel("<b>3. Ratio Simplification (A : B)</b>"))
        row3 = QHBoxLayout()
        self.ratio_a_input = QLineEdit("48")
        self.ratio_a_input.setProperty("class", "business-input")
        self.ratio_b_input = QLineEdit("64")
        self.ratio_b_input.setProperty("class", "business-input")
        self.ratio_res_label = QLabel("= 3 : 4")
        self.ratio_res_label.setStyleSheet("color: #0A84FF; font-weight: 700; font-size: 16px;")

        self.ratio_a_input.textChanged.connect(self._recalc_ratio)
        self.ratio_b_input.textChanged.connect(self._recalc_ratio)

        row3.addWidget(self.ratio_a_input)
        row3.addWidget(QLabel(":"))
        row3.addWidget(self.ratio_b_input)
        row3.addWidget(self.ratio_res_label)
        c3_layout.addLayout(row3)
        layout.addWidget(card3)

        layout.addStretch()
        scroll.setWidget(container)

        self._recalc_pct_of()
        self._recalc_pct_change()
        self._recalc_ratio()

        return scroll

    def _recalc_pct_of(self):
        try:
            x = self.pct_x_input.text()
            y = self.pct_y_input.text()
            res = self.engine.compute_percentage_of(x, y)
            self.pct_res_label.setText(f"= {res['fmt_result']}")
        except Exception:
            self.pct_res_label.setText("=")

    def _recalc_pct_change(self):
        try:
            old = self.chg_old_input.text()
            new = self.chg_new_input.text()
            res = self.engine.compute_percentage_change(old, new)
            t = res["type"]
            color = "#30D158" if t == "increase" else ("#FF453A" if t == "decrease" else "#989BA5")
            self.chg_res_label.setStyleSheet(f"color: {color}; font-weight: 700; font-size: 16px;")
            self.chg_res_label.setText(f"= {res['fmt_percentage']} {t}")
        except Exception:
            self.chg_res_label.setText("=")

    def _recalc_ratio(self):
        try:
            a = int(self.ratio_a_input.text().replace(",", "").strip())
            b = int(self.ratio_b_input.text().replace(",", "").strip())
            res = self.engine.compute_simplify_ratio(a, b)
            self.ratio_res_label.setText(f"= {res['simplified_ratio']}")
        except Exception:
            self.ratio_res_label.setText("=")

    def _copy_text(self, text: str, btn: QPushButton):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        orig = btn.text()
        btn.setText("✓ Copied!")
        QTimer.singleShot(1500, lambda: btn.setText(orig))
