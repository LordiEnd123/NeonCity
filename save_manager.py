import json
import os

SAVE_FILE = "save_data.json"


def load_progress():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return data.get("unlocked_levels", 1)
    return 1


def save_progress(unlocked_levels):
    with open(SAVE_FILE, "w") as f:
        json.dump({"unlocked_levels": unlocked_levels}, f)