"""Lab 7 - Hypothesis fuzz tests for customs_duty.py.

For each function:
  1. *No crash*: for ANY text (or None) the function must not raise - it returns
     a result for valid input and None for invalid input.
  2. *Correctness*: for well-formed generated input the result must be right.
"""
import math

from hypothesis import given, settings, strategies as st

from customs_duty import parse_declaration, duty_amount, hs_chapter

# Fuzz inputs: random unicode text, None, and "nearly valid" strings made of the
# characters these parsers care about (digits, ':', '@', '.', signs, nan/inf ...).
nearly_valid = st.text(alphabet="0123456789:@.-+ eEnaifNIbookslctr\t", max_size=30)
fuzz_input = st.text() | st.none() | nearly_valid


# ---------------- parse_declaration ----------------

@settings(max_examples=500)
@given(fuzz_input)
def test_parse_declaration_no_crash(s):
    try:
        result = parse_declaration(s)
    except Exception as e:  # noqa: BLE001 - any exception is a fuzzing failure
        assert False, f"parse_declaration crashed on {s!r} with: {e!r}"
    if result is not None:
        category, value = result
        assert category and math.isfinite(value) and value >= 0


@given(st.sampled_from(["electronics", "clothing", "books", "toys"]),
       st.integers(min_value=0, max_value=10**7), st.sampled_from(["", " "]))
def test_parse_declaration_valid(category, value, pad):
    text = f"{pad}{category.upper()}{pad}:{pad}{value}{pad}"
    assert parse_declaration(text) == (category, float(value))


# ---------------- duty_amount ----------------

@settings(max_examples=500)
@given(fuzz_input)
def test_duty_amount_no_crash(s):
    try:
        result = duty_amount(s)
    except Exception as e:  # noqa: BLE001
        assert False, f"duty_amount crashed on {s!r} with: {e!r}"
    # duty must never be negative, NaN or infinite
    assert result is None or (math.isfinite(result) and result >= 0)


@given(st.floats(min_value=0, max_value=1e9), st.floats(min_value=0, max_value=100))
def test_duty_amount_valid(value, rate):
    result = duty_amount(f"{value}@{rate}")
    assert result is not None
    assert math.isclose(result, value * rate / 100, abs_tol=0.01)
    assert result <= value + 0.01  # a rate of at most 100% never exceeds the value


# ---------------- hs_chapter ----------------

@settings(max_examples=500)
@given(fuzz_input)
def test_hs_chapter_no_crash(s):
    try:
        result = hs_chapter(s)
    except Exception as e:  # noqa: BLE001
        assert False, f"hs_chapter crashed on {s!r} with: {e!r}"
    assert result is None or 1 <= result <= 97  # HS chapters are 01-97


@given(st.integers(min_value=1, max_value=97), st.integers(min_value=0, max_value=99),
       st.integers(min_value=0, max_value=99))
def test_hs_chapter_valid(chapter, heading, sub):
    assert hs_chapter(f"{chapter:02d}{heading:02d}.{sub:02d}") == chapter
