import json
import os

def load_data_from_json(filename="projekt_data.json"):
    """Lädt die Daten aus der angegebenen JSON-Datei und gibt ein Dictionary zurück."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data_to_json(data, filename="projekt_data.json"):
    """Speichert das Dictionary `data` in einer JSON-Datei."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

