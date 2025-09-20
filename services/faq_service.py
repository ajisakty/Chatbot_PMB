import json
from config import FAQ_PATH

def load_faq():
    try:
        with open(FAQ_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_faq(faq_data):
    with open(FAQ_PATH, "w", encoding="utf-8") as f:
        json.dump(faq_data, f, indent=4, ensure_ascii=False)
