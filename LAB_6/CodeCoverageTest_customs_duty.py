"""Lab 6 - Code (line) coverage tests for customs_duty.py.

Goal: execute every line of customs_duty.py at least once (>= 90% line coverage).
"""
import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


# ---------------- duty_rate ----------------

def test_books_are_duty_free():
    assert duty_rate("books", "FTA") == 0


def test_prohibited_item_raises():
    with pytest.raises(ValueError, match="prohibited item"):
        duty_rate("weapons", "US")


def test_electronics_fta():
    assert duty_rate("electronics", "FTA") == 0.10


def test_electronics_non_fta():
    assert duty_rate("electronics", "US") == 0.20


def test_clothing_fta():
    assert duty_rate("clothing", "FTA") == 0.05


def test_clothing_non_fta():
    assert duty_rate("clothing", "CN") == 0.12


def test_other_category_default_rate():
    assert duty_rate("toys", "US") == 0.15


# ---------------- total_duty ----------------

def test_low_value_personal_import():
    assert total_duty("books", 500, "US", False) == 0


def test_negative_value_raises():
    with pytest.raises(ValueError, match="negative value"):
        total_duty("toys", -1, "US", False)


def test_small_gift_is_free():
    assert total_duty("electronics", 3000, "US", True) == 0


def test_large_gift_pays_on_value_above_5000():
    # (15000 - 5000) * 0.20
    assert total_duty("electronics", 15000, "US", True) == pytest.approx(2000)


def test_minimum_duty_of_50():
    # gift: (5500 - 5000) * 0.05 = 25 -> raised to the 50 minimum
    assert total_duty("clothing", 5500, "FTA", True) == 50


# ---------------- clearance_channel ----------------

def test_prohibited_is_refused():
    assert clearance_channel(100, "narcotics", True) == "refuse"


def test_very_high_value_is_inspected():
    assert clearance_channel(150000, "toys", True) == "inspect"


def test_high_value_without_documents_is_inspected():
    assert clearance_channel(30000, "toys", False) == "inspect"


def test_normal_goods_go_green():
    assert clearance_channel(5000, "books", True) == "green"
