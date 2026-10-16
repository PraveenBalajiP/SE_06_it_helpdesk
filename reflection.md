# Lab 5 - Static Code Analysis Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

**Easiest:** the style and quality findings Pylint reported: missing docstrings, `snake_case` naming, `== None` to `is None`, the unused variable, f-strings, `.items()`, and opening files with `with` and an encoding. Each had a clear message and a one-line fix with no change in behaviour.

**Hardest:** the security and behaviour issues. Removing the shell from the ping function meant adding hostname validation, an argument list, a timeout, and OS-specific flags, then thinking through attack inputs. Moving the admin password to an environment variable changed how ticket closing is configured. Urgency validation was not flagged by any tool and had to be found by running the program and testing odd inputs.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Yes, in the practical sense. After the fixes, Bandit still reports B404 (importing `subprocess`) and B603 (calling `subprocess.run`). Both are Low severity and Bandit warns about them for any subprocess use. In this code the command is an argument list, `shell=True` is not used, the hostname is validated with a regex, and a timeout is set, so they are not exploitable. I documented them in `issues.md` instead of suppressing them. Also, Bandit rated the hard-coded password (B105) only Low, even though in practice it was the most serious credential problem, so tool severity should be reviewed, not trusted blindly.

## 3. How would you integrate static analysis tools into your actual software development workflow?

I would run Flake8, Pylint, and Bandit locally before each commit, for example with a pre-commit hook, and again in CI (such as GitHub Actions) on every push and pull request, failing the build on Medium or High findings or on a Pylint score below a set threshold. Any warning that is deliberately accepted would be documented with a justification. Tools do not replace code review or testing, so I would use them alongside both.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- Pylint improved from 5.53/10 to 10.00/10, Flake8 reports no violations, and Bandit dropped from 1 High and 3 Low issues to 2 Low ones.
- Urgency and other inputs are validated, so bad data can no longer create invalid tickets.
- The admin password is no longer in the source code.
- The ping feature is no longer open to command injection.
- Errors are no longer silently swallowed, and the audit log no longer shares state between calls.
- Docstrings, consistent naming, and a `main()` guard make the code easier to read, test, and import.