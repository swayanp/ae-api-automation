"""
data_loader.py
----------------
This file defines utility functions to load external test data from CSV and JSON files.

Features:
- Read rows from a CSV file and return as list of dictionaries
- Read structured JSON files and return as Python dictionary
- Useful for data-driven testing (e.g., login tests, product search, etc.)
"""

import csv
import json
from pathlib import Path

def load_users_csv(path="data/users.csv"):
    """
    Loads user login test data from CSV and returns it as a list of dictionaries.

    Args:
        path (str): Relative path to CSV file

    Returns:
        List[dict]: Each row as a dictionary (column_name: value)
    """
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

def load_json_file(path: str) -> dict:
    """
    Loads and returns any JSON file as a dictionary.

    Args:
        path (str): Path to the JSON file

    Returns:
        dict: Parsed JSON data
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_products_data() -> dict:
    """
    Shortcut to load product test data from data/products.json
    """
    return load_json_file("data/products.json")
