import json

def load_lang(lang):
    with open(f"app/translations/{lang}.json", encoding="utf-8") as f:
        return json.load(f)
