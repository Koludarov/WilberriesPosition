import re


def contains_only_digits(string: str) -> bool:
    """Проверяет, состоит ли строка только из цифр"""
    pattern = r'^\d+$'
    return re.match(pattern, string) is not None
