# Code Health Audit - 2025-07-04

## Test Results
Pytest collected no tests. No failures or stack traces were produced.

## Ruff Findings
Ruff reported no issues.

## Bandit Findings
Bandit identified three Medium severity issues:

| Severity | Issue | Location |
|----------|-------|---------|
| Medium | B104 binding to all interfaces | `app.py:204` |
| Medium | B108 hardcoded temp directory | `config.py:27` |
| Medium | B113 request without timeout | `generate_docs.py:118` |

## Cyclomatic Complexity
One function exceeded a complexity score of 10:

| File | Function | Complexity |
|------|----------|-----------|
| `generate_docs.py` | `main` | 13 (C) |

## Recommendations
1. Add unit tests for configuration and blueprint registration to give pytest coverage.
2. Address the Bandit findings by avoiding binding to all interfaces, using configurable temp directories, and specifying timeouts on HTTP requests.
3. Break down `generate_docs.py:main` into smaller functions to reduce complexity.
