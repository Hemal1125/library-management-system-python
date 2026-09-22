"""
utils/validators.py
"""

import re


def is_valid_email(email: str) -> bool:
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email))


def is_valid_isbn(isbn: str) -> bool:
    # Accepts ISBN-10 or ISBN-13 (digits only, optional hyphens)
    cleaned = isbn.replace("-", "").strip()
    return cleaned.isdigit() and len(cleaned) in (10, 13)


def is_non_empty(value: str) -> bool:
    return bool(value and value.strip())