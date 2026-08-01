---
name: code-reviewer
description: Provides a structured review process and checklist for Python, SQL, Docker, and Airflow code in the PhilWeather ETL project.
---

# Purpose
Ensure code quality, consistency, and adherence to best‑practice standards across the entire weather ETL codebase.

# When to Use
- Before merging a pull request that touches ETL logic, DAGs, dbt models, or Dockerfiles.
- Conducting a quarterly code health audit.
- Enforcing style guidelines for new contributors.

# Responsibilities
- Run static analysis (`ruff`, `flake8`, `sqlfluff`).
- Verify unit/integration tests and coverage thresholds.
- Check security concerns (hard‑coded secrets, SQL injection).
- Validate documentation completeness (docstrings, README updates).
- Ensure CI pipeline passes all stages.

# Workflow
1. **Pre‑review Setup** – Checkout PR branch locally, install dependencies (`pip install -e .[dev]`).
2. **Static Analysis** – Execute `ruff check .` and `sqlfluff lint sql/`. Capture warnings.
3. **Run Tests** – `pytest -q --cov=philweather_etl` and ensure coverage > 85 %.
4. **Security Scan** – Search for secret patterns using `trufflehog` or regex for `AKIA`‑style keys.
5. **Documentation Check** – Verify module docstrings, update `CHANGELOG.md`, ensure new functions have examples.
6. **Review Comments** – Add inline comments on GitHub PR using the checklist below.
7. **Approve / Request Changes** – Approve if all checks pass; otherwise request specific fixes.

# Best Practices
- Keep each review focused on a single concern (style → tests → security).
- Use the "Four‑eye" principle for production‑critical changes.
- Encourage use of typed signatures and `pydantic` models.
- Prefer parametrised queries over string concatenation.
- Require at least one reviewer from a different component team.

# Anti‑patterns
- Approving without running the full test suite.
- Ignoring lint warnings to speed up merges.
- Over‑looking secret leakage in Dockerfiles or `.env` files.
- Accepting large PRs (> 500 lines) without breaking them into logical commits.

# Checklist
- [ ] Lint passes (`ruff`, `sqlfluff`).
- [ ] All new code has type hints and docstrings.
- [ ] Unit tests cover new logic (>80 %).
- [ ] Integration tests run against a local Docker PostgreSQL.
- [ ] No secrets or passwords present in code or Dockerfiles.
- [ ] Updated README/CHANGELOG for user‑visible changes.
- [ ] CI pipeline (GitHub Actions) succeeds.

# Examples
```bash
# Run review locally
git checkout feature/new-loader
pip install -e .[dev]
ruff check . && sqlfluff lint sql/
pytest -q --cov=philweather_etl
trufflehog filesystem .
```

# Project‑Specific Guidance
- Use the `philweather_etl/lint/` config which extends the shared `ruff` config with Supabase‑specific rules.
- Dockerfile linting: run `hadolint Dockerfile` for each service image.
- Airflow DAGs must have `owner`, `email_on_failure`, and `retries` defined.
- After review, add the `reviewed-by` label to the PR for audit trails.
