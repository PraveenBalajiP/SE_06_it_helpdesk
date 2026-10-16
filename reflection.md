# Lab 5 — Static Code Analysis Reflection

## 1. Which fixes were easiest and hardest, and why?

The easiest fixes were code-style improvements and file handling. For example, adding a context manager for file operations and following consistent naming and formatting conventions were straightforward.

The harder fixes involved security and program behaviour. Replacing the hard-coded administrator password with an environment variable required changes to how ticket closure is configured. Revising the ping functionality required attention to input validation, command execution, and timeout handling. Urgency validation also needed to ensure that invalid values could not create tickets with inappropriate priorities.

## 2. Did any tools report false positives?

Bandit reported two Low-severity findings: B404 for importing `subprocess` and B603 for calling `subprocess.run()`.

These findings are warnings that require review rather than proof of an exploitable vulnerability. The helpdesk system uses subprocess functionality for its ping feature. The corrected implementation passes command arguments as a list, does not enable shell execution, validates the hostname, and sets a timeout.

The warnings were therefore documented and reviewed instead of being suppressed. No Medium- or High-severity Bandit findings remained in the final report.

## 3. How could static analysis tools be integrated into the development workflow?

Pylint, Bandit, and Flake8 can be run before committing changes to the repository. Their commands can also be added to a GitHub Actions workflow so that each push or pull request triggers automated checks.

Developers should review the reports, correct genuine issues, and document any remaining warnings with a clear justification. Running the tools consistently helps detect problems earlier and reduces the effort required during code review.

## 4. What tangible improvements were achieved?

The corrections improved the helpdesk program in several ways:

- Urgency values are validated and restricted to the range 1–5.
- The administrator password is obtained from an environment variable rather than being stored directly in the source code.
- The ping feature avoids shell-based command execution and includes input validation and a timeout.
- The audit log no longer uses a mutable default argument.
- Invalid or empty input is handled more consistently.
- File operations use a context manager and explicit UTF-8 encoding.
- The program has a main-entry guard, allowing its functions to be imported without automatically running the demonstration.
- Pylint reached 10.00/10, Flake8 reported no violations, and Bandit reported no Medium- or High-severity findings.

Overall, the exercise improved code quality, input handling, and security awareness while demonstrating how static analysis can support software maintenance.
