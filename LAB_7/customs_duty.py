"""Customs duty helpers - hardened against invalid input (Lab 7 fuzzing fixes).

Every public function returns None instead of raising when the input is invalid.
"""
import math

MAX_NUMBER_LENGTH = 32  # very long numeric strings are rejected before float()


def _non_negative_number(token):
    """Return token as a finite float >= 0, or None."""
    token = token.strip()
    if not token or len(token) > MAX_NUMBER_LENGTH:
        return None
    try:
        value = float(token)
    except ValueError:
        return None
    if not math.isfinite(value) or value < 0:  # rejects nan, inf and negatives
        return None
    return value


def parse_declaration(text):
    """'electronics:25000' -> ('electronics', 25000.0). None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    category = parts[0].strip().lower()
    if not category or not category.replace(' ', '').isalpha():
        return None
    value = _non_negative_number(parts[1])
    if value is None:
        return None
    return category, value


def duty_amount(text):
    """'25000@20' -> 5000.0 (value x rate%). None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split('@')
    if len(parts) != 2:
        return None
    value = _non_negative_number(parts[0])
    rate = _non_negative_number(parts[1])
    if value is None or rate is None or rate > 100:  # a duty rate is 0-100 %
        return None
    amount = value * rate / 100
    if not math.isfinite(amount):  # e.g. 1e308 * 100 overflows to inf
        return None
    return round(amount, 2)


def hs_chapter(code):
    """'8517.12' -> 85 (first two digits). None for invalid input."""
    if not isinstance(code, str):
        return None
    heading = code.strip().split('.')[0]
    # need at least 2 plain ASCII digits; HS chapters run from 01 to 97
    if len(heading) < 2 or not heading.isascii() or not heading.isdigit():
        return None
    chapter = int(heading[:2])
    if not 1 <= chapter <= 97:
        return None
    return chapter


def _show(label, result):
    if result is None:
        print(f"{label}: Invalid input, please check the format.")
    else:
        print(f"{label}:", result)


def main():
    print("==== Running parse_declaration ====")
    user_input = input("Enter category:value (e.g. electronics:25000): ")
    _show("Category and Value", parse_declaration(user_input))

    print("\n==== Running duty_amount ====")
    user_input = input("Enter value@rate (e.g. 25000@20): ")
    _show("Duty Amount", duty_amount(user_input))

    print("\n==== Running hs_chapter ====")
    user_input = input("Enter an HS code (e.g. 8517.12): ")
    _show("Chapter", hs_chapter(user_input))


if __name__ == "__main__":
    main()
