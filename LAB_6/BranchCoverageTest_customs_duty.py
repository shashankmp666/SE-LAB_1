"""Lab 6 - Branch coverage tests for customs_duty.py.

Goal: take every decision (if / elif) both the True and the False way
(>= 90% branch coverage), including boundary values.
"""
import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


# ---------------- duty_rate ----------------

@pytest.mark.parametrize("category", ["weapons", "narcotics"])
def test_prohibited_categories_raise(category):              # line 5: True
    with pytest.raises(ValueError, match="prohibited item"):
        duty_rate(category, "FTA")


@pytest.mark.parametrize("category, origin, rate", [
    ("electronics", "FTA", 0.10),   # line 7 True, line 8 True
    ("electronics", "US", 0.20),    # line 7 True, line 8 False
    ("clothing", "FTA", 0.05),      # line 11 True, line 12 True
    ("clothing", "CN", 0.12),       # line 11 True, line 12 False
    ("books", "US", 0),             # line 15 True
    ("toys", "FTA", 0.15),          # line 15 False -> default rate
    ("Electronics", "FTA", 0.15),   # categories are case-sensitive
])
def test_duty_rate_every_branch(category, origin, rate):
    assert duty_rate(category, origin) == rate


# ---------------- total_duty ----------------

def test_negative_value_raises():                            # line 21: True
    with pytest.raises(ValueError, match="negative value"):
        total_duty("toys", -0.01, "US", False)


def test_zero_value_is_free():                               # line 21: False (boundary 0)
    assert total_duty("toys", 0, "US", False) == 0


def test_gift_at_5000_limit_is_free():                       # line 23 True, line 24 True
    assert total_duty("electronics", 5000, "US", True) == 0


def test_gift_above_5000_pays_on_excess():                   # line 24 False
    assert total_duty("electronics", 15000, "US", True) == pytest.approx(2000)


def test_personal_import_at_1000_limit_is_free():            # line 23 False, line 27 True
    assert total_duty("electronics", 1000, "US", False) == 0


def test_personal_import_above_1000_pays_full():             # line 27 False
    assert total_duty("electronics", 2000, "US", False) == pytest.approx(400)


def test_duty_below_50_is_raised_to_minimum():               # line 30 True
    assert total_duty("clothing", 5500, "FTA", True) == 50


def test_zero_duty_stays_zero():                             # line 30 False (duty == 0)
    assert total_duty("books", 8000, "US", False) == 0


def test_duty_exactly_50_unchanged():                        # line 30 False (boundary 50)
    # gift: (6000 - 5000) * 0.05 = 50
    assert total_duty("clothing", 6000, "FTA", True) == pytest.approx(50)


def test_prohibited_item_raises_through_total_duty():
    with pytest.raises(ValueError):
        total_duty("weapons", 2000, "US", False)


# ---------------- clearance_channel ----------------

def test_prohibited_is_refused():                            # line 36: True
    assert clearance_channel(10, "weapons", True) == "refuse"


def test_above_100000_is_inspected():                        # line 38: True
    assert clearance_channel(100001, "toys", True) == "inspect"


def test_exactly_100000_with_documents_is_green():           # line 38 False, 40 False (has docs)
    assert clearance_channel(100000, "toys", True) == "green"


def test_above_20000_without_documents_is_inspected():       # line 40: True
    assert clearance_channel(20001, "toys", False) == "inspect"


def test_exactly_20000_without_documents_is_green():         # line 40 False (value boundary)
    assert clearance_channel(20000, "toys", False) == "green"
