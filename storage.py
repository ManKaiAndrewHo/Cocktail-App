import json
import os

DATA_FILE = "user_data.json"

def load_user_data():
    if not os.path.exists(DATA_FILE):
        return {
            "recipes": [],
            "favorites": [],
            "version": 1
        }

    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_user_data(user_data):
    with open(DATA_FILE, "w") as f:
        json.dump(user_data, f, indent=4)
