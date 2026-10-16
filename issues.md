# Lab 5 — Static Code Analysis Issues Report

## 1. Project Information

- **Project:** IT Helpdesk System
- **Target file:** `helpdesk_system.py`
- **Tools:** Pylint, Bandit, and Flake8
- **Objective:** Identify code-quality and security issues, correct them, and verify the updated program.

## 2. Issues Identified and Fixes

| No. | Original issue | Severity | Correction | Status |
|---:|---|---|---|---|
| 1 | Mutable default argument used for the audit log | Medium | Changed the default to `None` and selected the log inside the function | Fixed |
| 2 | Administrator password hard-coded in source code | High | Read the password from the `HELPDESK_ADMIN_PASSWORD` environment variable | Fixed |
| 3 | Ping command constructed using shell execution | High | Used a subprocess argument list without `shell=True` and added hostname validation and a timeout | Fixed |
| 4 | Urgency values were not restricted to the valid range | Medium | Added validation requiring an integer from 1 to 5 | Fixed |
| 5 | Bare exception handling could hide errors | Medium | Replaced it with explicit validation and exception handling | Fixed |
| 6 | File handling lacked an explicit context manager and encoding | Low | Used `with open(...)` and UTF-8 encoding | Fixed |
| 7 | Missing input validation for user names, issue types, technicians, and notes | Medium | Added checks for invalid or empty inputs | Fixed |
| 8 | Main program executed when the module was imported | Low | Added an `if __name__ == "__main__":` guard | Fixed |

*Severity values above are the project's assessment of the original code-review findings, not necessarily the severity assigned by a static-analysis tool.*

## 3. Final Static Analysis Results

### Pylint
- Final score: **10.00/10**
- No Pylint messages were reported in the final output.

### Flake8
- Final output: empty.
- No Flake8 violations were reported.

### Bandit
- Total reported issues: 2
- Low severity: 2
- Medium severity: 0
- High severity: 0

| Bandit ID | Finding | Severity | Assessment |
|---|---|---|---|
| B404 | Use of the `subprocess` module | Low | Required for the ping functionality; reviewed |
| B603 | Use of `subprocess.run()` | Low | Command arguments are passed as a list, shell execution is disabled, hostname input is validated, and a timeout is set |

The two Bandit warnings remain visible in the final report. They are documented rather than suppressed.

## 4. Conclusion

The corrected program passes Pylint with a score of 10.00/10 and produces no Flake8 violations. Bandit reports two Low-severity subprocess-related warnings and no Medium- or High-severity findings. The code changes improve input validation, credential handling, exception handling, and subprocess safety.
