"""Constants used across the Modern Multi-Mode Calculator application."""

import math

# Mathematical Constants
PI = math.pi
E = math.e
# Golden Ratio: phi = (1 + sqrt(5)) / 2
PHI = (1.0 + math.sqrt(5.0)) / 2.0

# Angle Modes
ANGLE_DEG = "DEG"
ANGLE_RAD = "RAD"
ANGLE_GRAD = "GRAD"

# Currencies
CURRENCIES = {
    "INR": {"symbol": "₹", "name": "Indian Rupee", "code": "INR"},
    "USD": {"symbol": "$", "name": "US Dollar", "code": "USD"},
    "EUR": {"symbol": "€", "name": "Euro", "code": "EUR"},
    "GBP": {"symbol": "£", "name": "British Pound", "code": "GBP"},
    "JPY": {"symbol": "¥", "name": "Japanese Yen", "code": "JPY"},
}

DEFAULT_CURRENCY = "INR"

# Calculator Modes
MODE_STANDARD = "standard"
MODE_SCIENTIFIC = "scientific"
MODE_BUSINESS = "business"

# Standard GST Rates in India
GST_RATES = [0, 5, 12, 18, 28]
DEFAULT_GST_RATE = 18

# Compounding Frequencies
COMPOUND_FREQUENCIES = {
    "Annually": 1,
    "Half-Yearly": 2,
    "Quarterly": 4,
    "Monthly": 12,
    "Daily": 365,
}
