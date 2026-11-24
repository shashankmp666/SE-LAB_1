# L6_L7_35 — Customs Duty Calculator

Lab 7: Fuzz Testing

## About

A small Python module that reads customs declarations, computes duty and extracts tariff chapters.

## Files

| File | Description |
|------|-------------|
| `customs_duty.py` | The code under test |
| `test_customs_duty.py` | Starter test file |

Refer to the lab handout for instructions.

---

## Lab 7 Submission (PES1UG24AM160)

| File | Description |
|------|-------------|
| `customs_duty.py` | Fixed (hardened) application: returns `None` for invalid input instead of crashing |
| `test_customs_duty.py` | Hypothesis fuzz tests (no-crash + correctness properties for all three functions) |
| `Lab7_FuzzTesting_Screenshots.pdf` | Screenshots: buggy run, failing tests, fixed run, passing tests |
| `screenshots/` | The same screenshots as PNG files |

Run:
```
pip install hypothesis pytest
python customs_duty.py
python -m pytest test_customs_duty.py
```
