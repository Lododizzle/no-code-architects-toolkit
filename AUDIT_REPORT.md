# Code Health Audit - 2025-07-04

## Test Results
No tests were discovered when running `pytest -q`.

## Ruff Findings
Ruff reported no lint violations.

## Bandit Findings
All findings were medium severity:
1. **B104** `app.py:204` binds to all network interfaces.
2. **B108** `config.py:27` uses a hardcoded temp directory.
3. **B113** `generate_docs.py:118` performs a request without a timeout.

## Cyclomatic Complexity
Function `generate_docs.py:main` has complexity 13.
All other functions were below the threshold of 10.

## Recommendations
1. Add unit tests so `pytest` can validate application behaviour.
2. Fix the Bandit issues by restricting host binding, using configurable paths and adding HTTP timeouts.
3. Break up `generate_docs.py:main` into smaller helpers to reduce complexity and improve maintainability.

