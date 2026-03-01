# Logger —> appends every user action to data/logs.json.


import json
import os
from datetime import datetime


class Logger:

    _BASE     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGS_FILE = os.path.join(_BASE, "data", "logs.json")

    def _ensure_file(self):
        #Creates logs.json with an empty list if it does not exist yet.
        os.makedirs(os.path.dirname(self.LOGS_FILE), exist_ok=True)
        if not os.path.exists(self.LOGS_FILE):
            with open(self.LOGS_FILE, "w") as f:
                json.dump([], f, indent=2)

    def _read(self) -> list:
        #Loads and returns all existing log entries.
        self._ensure_file()
        with open(self.LOGS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def _write(self, logs: list):
        #Saves the full log list back to disk.
        with open(self.LOGS_FILE, "w") as f:
            json.dump(logs, f, indent=2)


    def log(self, email: str, action: str):
        #Appends one timestamped entry to logs.json.

        logs = self._read()
        logs.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "email":     email,
            "action":    action,
        })
        self._write(logs)

    def get_all(self) -> list:
        #Returns all log entries sorted newest-first.
        return list(reversed(self._read()))
