# Lab 5: Reflection

**Name:** M P Shashank  **SRN:** PES1UG24AM160

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest were the Flake8 whitespace errors (E225, E231, E261, E305) and the Pylint naming and docstring warnings.
Each one has a single obvious fix and nothing else depends on it. Renaming `trackParcel` to `track_parcel` and so on
only needed the callers in `main()` updated.

The hardest was the shell injection in `pingHub` (Bandit B602). Removing `shell=True` alone was not enough: I also
had to pass the command as a list, find the real `ping` executable, and validate the host address, so that the
function still works for real hostnames but refuses input like `"8.8.8.8; del *"`. The other hard one was a bug no
tool reported: `isWithCourier` said a parcel that is "Out for Delivery" is no longer with the courier. I only found it
by thinking about what each delivery stage means, not from any report.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

Yes. **B404** ("consider possible security implications associated with the subprocess module") is raised just because
`subprocess` is imported. After the fix the module is used safely (fixed argument list, no shell, validated input), but
Bandit would still flag the import. I documented it with `# nosec B404` and a reason instead of removing a feature.

**B311** is also context-dependent: `random` is fine for things like shuffling a demo list. Here the warning was real,
because the number is a delivery OTP that must not be guessable.

### 3. How would you integrate static analysis tools into your actual software development workflow?

- Run Flake8 and Pylint in the editor (VS Code extensions) so problems show up while typing.
- Add a **pre-commit hook** that runs Flake8 and Bandit, so badly formatted or obviously insecure code cannot be
  committed.
- Run all three tools in **CI** (for example GitHub Actions) on every pull request. Fail the build on any Bandit
  High/Medium finding or a Pylint score below an agreed threshold such as 9.0.
- Keep a shared config (`.pylintrc`, `setup.cfg`) in the repo so everyone uses the same rules. Any `# nosec` /
  `# pylint: disable` must carry a written reason that reviewers check.

### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Security:** Bandit went from 4 issues (1 High, 1 Medium) to 0. The hub ping can no longer run injected commands,
  temporary label files cannot be hijacked, and OTPs are no longer predictable.
- **Correctness:** parcels that are out for delivery are now correctly reported as with the courier. Invalid weights
  are rejected, and `book_parcel` no longer shares one history list between calls.
- **Readability:** consistent snake_case names and a docstring on every function make the file read like normal
  Python. The Pylint score went from 4.91 to 10.00 and Flake8 reports nothing.
- **Maintainability:** the `main()` guard means the module can be imported and tested without running the demo, and
  catching `KeyError` instead of `Exception` means real errors are no longer silently hidden.

The demo output (routes, statuses, costs 95.0 / 50 / 140, the unknown-id message) is unchanged, so the program still
does its job.
