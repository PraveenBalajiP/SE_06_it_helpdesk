# Lab 5 - Static Code Analysis Issues Report

**Project:** IT Helpdesk System | **File:** `helpdesk_system.py` | **Tools:** Pylint, Bandit, Flake8

## 1. Baseline (original code)

| Tool | Result on original code | Report |
|---|---|---|
| Pylint | 5.53/10, 21 messages | `reports/before/pylint_before.txt` |
| Bandit | 4 issues (1 High, 3 Low) | `reports/before/bandit_before.txt` |
| Flake8 | See report if present | `reports/before/flake8_before.txt` |

## 2. Issue table (High and Medium first)

Line numbers refer to the ORIGINAL file. "-" means the problem was found by running the program or by review, not flagged by a tool.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Shell command injection in ping | Security - High (Bandit B602) | 38 | Hostname was concatenated into a command run with `shell=True`, so input like `x; del ...` could run arbitrary commands | Removed `shell=True`; pass an argument list; validate hostname with a regex; added a 10 s timeout and OS-specific ping flag |
| Hard-coded admin password | Security - High (Bandit B105, tool rated Low) | 8 | Password stored in plain text in source code | Read from `HELPDESK_ADMIN_PASSWORD` environment variable; ticket closing is disabled if it is not set |
| Mutable default argument | Bug - Medium (Pylint W0102) | 10 | The audit-log list default was shared across all calls | Default changed to `None`; the log is chosen inside the function |
| Bare `except` with `pass` | Bug - Medium (Pylint W0702, Bandit B110) | 23 | Every error in `add_note` was silently swallowed, including invalid ticket IDs | Removed; explicit checks now return `False` for bad input |
| Urgency not validated | Bug - Medium (found by running) | - | Non-numeric or out-of-range urgency was accepted | Added `validate_urgency()` (integer 1-5, raises `ValueError`) and handled it in `main()` |
| Missing input validation | Bug - Medium (review) | - | Empty or non-string user, issue, technician, or note values were accepted | Added checks and trimming for all inputs |
| Global statement and constant naming | Quality - Low (Pylint W0603, C0103) | 7, 11 | Counter was a global modified via `global` and badly named | Replaced with `itertools.count` and `next()` |
| File opened without `with` / encoding | Bug - Low (Pylint R1732, W1514) | 41 | File handle could leak; encoding was platform-dependent | `with open(..., encoding="utf-8")` |
| `== None` and dict iteration | Style - Low (Pylint C0121, C0206) | 32-33 | Wrong None comparison; iterating keys then indexing | Used `is None` and `.items()` |
| Unused variable | Quality - Low (Pylint W0612) | 47 | Variable `t2` assigned but never used | Removed |
| Function not snake_case | Style - Low (Pylint C0103) | 30 | `unresolvedHighPriority` | Renamed to `unresolved_high_priority` |
| Missing docstrings | Style - Low (Pylint C0114, C0116) | 1, 10, 17, 20, 26, 30, 37, 40, 45 | Module and functions undocumented | Added docstrings |
| Long line / string formatting | Style - Low (Pylint C0301, C0209) | 13, 14 | 118-character line; `%`/concatenation formatting | Wrapped lines; used f-strings |
| Code ran on import | Design - Low (review) | - | Demo logic executed when the module was imported | Moved into `main()` behind `if __name__ == "__main__":` |

*Severity in the Type column is the project's own assessment; where a tool rated it differently, the tool's rating is noted.*

## 3. Final results (after fixes)

| Tool | Before | After | Report |
|---|---|---|---|
| Pylint | 5.53/10 | **10.00/10** | `reports/after/pylint_after.txt` |
| Bandit | 4 issues (1 High, 3 Low) | 2 issues (0 High, 0 Medium, 2 Low) | `reports/after/bandit_after.txt` |
| Flake8 | see baseline | **0 violations** | `reports/after/flake8_after.txt` |

### Remaining Bandit findings (reviewed, not suppressed)

| ID | Finding | Severity | Assessment |
|---|---|---|---|
| B404 | `import subprocess` | Low | Needed for the ping feature |
| B603 | `subprocess.run()` call | Low | Argument list, no shell, validated hostname, 10 s timeout |

## 4. Conclusion

All High and Medium issues were fixed and verified by re-running all three tools. The two remaining Low Bandit warnings are inherent to using `subprocess` and are mitigated and documented.