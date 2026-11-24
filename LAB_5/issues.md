# Lab 5: Static Code Analysis - Issue Table

**Name:** M P Shashank  **SRN:** PES1UG24AM160
**File:** `parcel_tracker.py` (repo `L5_35_parcel_tracker`)

| Metric | Before | After |
|---|---|---|
| Pylint score | 4.91/10 | **10.00/10** |
| Bandit issues | 4 (1 High, 1 Medium, 2 Low) | **0** |
| Flake8 issues | 4 | **0** |

Full tool output: `reports/before/` and `reports/after/`. Line numbers below refer to the **original** file.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (B602) | Security - **High** | 55 | `pingHub` builds `"ping -c 1 " + hubAddress` and runs it with `shell=True`. An address like `x; rm -rf ~` would run a second command. | Pass an argument list (`[ping, "-c", "1", host]`) with no shell, find `ping` with `shutil.which`, and reject anything that is not a plain hostname/IP using a regex. |
| Insecure temp file (B306) | Security - **Medium** | 50 | `tempfile.mktemp()` only returns a name; another process can create that file first (race condition / symlink attack). | Use `tempfile.mkstemp()`, which creates the file atomically, and close the returned descriptor. |
| Predictable delivery OTP (B311) | Security - Low | 72 | The OTP is made with `random.randint`, which is not cryptographically secure, so OTPs can be predicted. | Use `secrets.randbelow(9000) + 1000`. |
| Out-for-delivery parcel reported "not with courier" | Logic bug (not flagged by any tool) | 45 | `isWithCourier` only accepts "Picked Up" and "In Transit", so a parcel that is "Out for Delivery" (still in the courier's van) returns `False`. | Use a `COURIER_STATUSES` set that includes "Out for Delivery". |
| Mutable default argument (W0102) | Bug risk - Medium | 11 | `history=[]` is created once and shared between every call, so ids from earlier bookings leak into later ones. | Default to `None` and create a new list inside the function. |
| Catching too general exception (W0718) | Code quality - Medium | 37 | `except Exception` in `trackParcel` hides any error, not just a missing id. | Catch only `KeyError`. |
| No weight validation | Logic (not flagged) | 27-31 | `shippingCost(0)` or a negative weight still returns the base fee of 50. | Raise `ValueError` for weight <= 0. |
| subprocess import (B404) | Security - Low | 2 | Bandit warns whenever `subprocess` is imported. | Kept (needed for `ping_hub`), now only used safely; documented with `# nosec B404`. |
| camelCase names (C0103) | Style | 11-67 | Functions, arguments and variables use camelCase (`bookParcel`, `trackingId`, ...). | Renamed to snake_case (`book_parcel`, `tracking_id`, ...). |
| Missing docstrings (C0114/C0116) | Style | 1, 11-58 | No module or function docstrings. | Added a docstring to the module and every function. |
| Comparison chain (R1714) | Refactor | 45 | `status == "Picked Up" or status == "In Transit"`. | `status in COURIER_STATUSES`. |
| `main()` runs on import | Code quality | 75 | `main()` is called at module level, so importing the file runs the demo. | Wrapped in `if __name__ == "__main__":`. |
| Whitespace (E225, E231, E261, E305) | Style (Flake8) | 28, 71, 74, 75 | Missing spaces around `=` and after `,`, one space before an inline comment, missing blank lines before the top-level call. | Reformatted to PEP 8. |
