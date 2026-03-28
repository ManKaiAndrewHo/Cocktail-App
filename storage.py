import json
# import random
# import string
# from pathlib import Path
import os

DATA_FILE = "user_data.json"
CURRENT_VERSION = 2

def load_user_data():
    if not os.path.exists(DATA_FILE):
        return {"recipes": [], "favorites": [], "version": CURRENT_VERSION}
    with open(DATA_FILE, "r") as f:
        return json.load(f)
    
def save_user_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# def load_user_data():
#     if not Path(DATA_FILE).exists():
#         return create_default_data()

#     with open(DATA_FILE, "r") as f:
#         data = json.load(f)

#     if data.get("version") != CURRENT_VERSION:
#         data = migrate_data(data)

#     return data

# def save_user_data(data):
#     with open(DATA_FILE, "w") as f:
#         json.dump(data, f, indent=4)

# def create_default_data():
#     data = {
#         "version": CURRENT_VERSION,
#         "recipes": [],
#         "favorites": []
#     }
#     save_user_data(data)
#     return data

# def migrate_data(data):
#     # placeholder for future-you
#     data["version"] = CURRENT_VERSION
#     return data

# def generate_id(length=8):
#     chars = string.ascii_letters + string.digits
#     return ''.join(random.choice(chars) for _ in range(length))

# def get_recipe_by_id(user_data, recipe_id):
#     for recipe in user_data["recipes"]:
#         if recipe["id"] == recipe_id:
#             return recipe
#     return None