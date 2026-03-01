# Logger —> appends every user action to data/logs.json.


import json
import os
from datetime import datetime


class Logger:
    LOG_FILE = "data/logs.json"

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.LOG_FILE):
            with open(self.LOG_FILE, "w") as f:
                json.dump([], f)

    def log(self, email, action):
        """Save a log entry safely"""
        try:
            with open(self.LOG_FILE, "r") as f:
                logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []

        logs.append({
            "email": email,
            "action": action,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        with open(self.LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)