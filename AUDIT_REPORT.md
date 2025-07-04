# Code Health Audit - 2025-07-04

## Test Results
No tests were collected, so no failures or stack traces to report.

## Ruff Findings
All checks passed with no violations.

## Bandit Findings
The scan identified three Medium severity issues:

| Severity | Count | Details |
|----------|-------|---------|
| Medium   | 3     | B104 binding to all interfaces in `app.py:204`, B108 hardcoded temp directory in `config.py:27`, B113 request without timeout in `generate_docs.py:118` |

## Cyclomatic Complexity
Only one function exceeded a complexity of 10:

| File | Function | Complexity |
|------|----------|-----------|
| generate_docs.py | `main` | 13 (C) |

## Recommendations
1. Add unit tests for configuration and blueprint registration to give pytest coverage.
2. Address the Bandit findings by avoiding binding to all interfaces, using configurable temp directories, and specifying timeouts on HTTP requests.
3. Break down `generate_docs.py:main` into smaller functions to reduce complexity.
