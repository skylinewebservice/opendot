import json
from pathlib import Path
from django.conf import settings

def get_products():
    file_path = Path(settings.BASE_DIR) / 'products.json'
    with open(file_path) as f:
        data = json.load(f)
        return data.get('products', [])

def get_products():
    try:
        with open('products.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    if isinstance(data, dict):
        return data.get('products', [])
    else:
        return []