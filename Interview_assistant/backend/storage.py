# backend/storage.py
import os
import json
from backend.models import HISTORY_FILE, USER_DETAILS_FILE

def load_chat_history():
    return json.load(open(HISTORY_FILE, "r")) if os.path.exists(HISTORY_FILE) else []

def save_chat_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def clear_chat_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

def save_user_details(details):
    with open(USER_DETAILS_FILE, "w") as f:
        json.dump(details, f)

def get_user_details():
    if os.path.exists(USER_DETAILS_FILE):
        try:
            with open(USER_DETAILS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}