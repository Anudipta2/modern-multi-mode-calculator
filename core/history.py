"""Calculation history management with local JSON persistence."""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class HistoryManager:
    """Manages session and persistent calculation history."""

    def __init__(self, storage_file: Optional[str] = None):
        if storage_file is None:
            # Default to AppData or user home directory
            app_data = os.environ.get("APPDATA") or os.path.expanduser("~")
            dir_path = os.path.join(app_data, "ModernCalculator")
            try:
                os.makedirs(dir_path, exist_ok=True)
                self.storage_file = os.path.join(dir_path, "calc_history.json")
            except OSError:
                self.storage_file = os.path.expanduser("~/.modern_calculator_history.json")
        else:
            self.storage_file = storage_file

        self._entries: List[Dict[str, str]] = []
        self.load_history()

    def add_entry(self, expression: str, result: str, mode: str = "standard") -> Dict[str, str]:
        """Add a calculation record to history and save."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "expression": str(expression).strip(),
            "result": str(result).strip(),
            "mode": mode,
            "timestamp": now,
        }
        # Prepend so newest is at the top
        self._entries.insert(0, entry)
        # Limit history to 200 entries to maintain high performance
        if len(self._entries) > 200:
            self._entries = self._entries[:200]
        self.save_history()
        return entry

    def get_entries(self, mode: Optional[str] = None) -> List[Dict[str, str]]:
        """Get history entries, optionally filtered by mode."""
        if mode:
            return [e for e in self._entries if e.get("mode") == mode]
        return list(self._entries)

    def remove_entry(self, index: int) -> bool:
        """Remove a specific entry by index."""
        if 0 <= index < len(self._entries):
            del self._entries[index]
            self.save_history()
            return True
        return False

    def clear(self):
        """Clear all history."""
        self._entries = []
        self.save_history()

    def save_history(self):
        """Save history to JSON file."""
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self._entries, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # Avoid crashing on disk permission issues

    def load_history(self):
        """Load history from JSON file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self._entries = data
            except Exception:
                self._entries = []
