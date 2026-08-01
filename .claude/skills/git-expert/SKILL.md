---
name: git-expert
description: Provides advanced Git workflows, branching strategies, and repository hygiene guidance for the PhilWeather ETL project.
---

# Purpose
Standardise version control practices, enforce commit quality, and streamline collaboration for the weather data pipeline codebase.

# When to Use
- Initialising the repository or adding a new remote.
- Implementing feature branches, release branches, or GitFlow.
- Conducting code reviews, rebasing, and squashing commits.
- Managing large binary assets (e.g., migration dumps) with Git LFS.
- Automating release tagging and changelog generation.

# Responsibilities
- Define branch naming conventions (`feature/<ticket>`, `hotfix/<issue>`).
- Enforce commit message format (Conventional Commits).
- Configure protected branches and required status checks in GitHub.
- Set up pre‑commit hooks for linting, secret scanning, and formatting.
- Provide guidelines for handling merge conflicts and rebases.
- Maintain a `CHANGELOG.md` automatically via `git-cliff` or similar.

# Workflow
1. **Repository Setup** – Run `git init` (if not already) and add remote `origin`.
2. **Branch Policy** – `main` is protected; develop on `develop`.
3. **Feature Development** – Create `feature/<JIRA‑ID>-<short-description>` branch from `develop`.
4. **Commit Discipline** – Use `git commit -m "feat(scope): description"` following Conventional Commits.
5. **Pre‑commit Hooks** – Run `pre-commit install` (hooks: ruff, black, sqlfluff, trufflehog).
6. **Pull Request** – Open PR against `develop`; required checks: lint, tests, code‑reviewer checklist.
7. **Rebase / Squash** – Before merging, rebase onto latest `develop` and squash commits to a single logical unit.
8. **Release** – Create a `release/<version>` branch, run integration tests, then merge to `main` and tag `vX.Y.Z`.
9. **Changelog** – Generate with `git-cliff --tag vX.Y.Z > CHANGELOG.md` and commit.
10. **Cleanup** – Delete feature branches after merge.

# Best Practices
- Keep commits small and focused; one logical change per commit.
- Never commit generated files (e.g., compiled `.pyc`, `node_modules`).
- Use signed commits (`git commit -S`) for security‑critical repos.
- Store large files (>5 MB) with Git LFS and track them via `.gitattributes`.
- Review diffs for accidental secret leakage before pushing.

# Anti‑patterns
- Direct commits to `main` bypassing review.
- Large merge commits that obscure individual changes.
- Rewriting public history on shared branches.
- Ignoring pre‑commit hook failures.
- Storing database credentials in plain text within the repo.

# Checklist
- [ ] Repository has `.gitignore` covering `__pycache__`, `*.egg-info`, `*.env`.
- [ ] `pre-commit` configured with hooks for lint, formatting, and secret scanning.
- [ ] Branch protection rules enabled on GitHub (`main`, `develop`).
- [ ] Commit message follows Conventional Commits.
- [ ] Pull request includes required reviewers and passes CI.
- [ ] Release tags are signed and follow semantic versioning.
- [ ] `CHANGELOG.md` updated automatically.

# Examples
```bash
# Create a new feature branch
git checkout -b feature/PHW-123-add-precipitation

# Make a commit
git add src/etl/precipitation.py
git commit -m "feat(precipitation): add precipitation ingestion"

# Rebase onto develop before PR
git fetch origin
git rebase origin/develop

# Push and open PR
git push -u origin feature/PHW-123-add-precipitation
```

```yaml
# .pre-commit-config.yaml (excerpt)
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.0
    hooks:
      - id: black
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.2.0
    hooks:
      - id: ruff
  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 2.3.4
    hooks:
      - id: sqlfluff-lint
  - repo: https://github.com/trufflesecurity/trufflehog
    rev: v3.52.0
    hooks:
      - id: trufflehog
```

# Project‑Specific Guidance
- The PhilWeather ETL repo lives at `git@github.com:emanuelcruzat/PhilWeather-ETL.git`.
- All contributors must sign the Contributor License Agreement (CLA) before merging.
- Use the `release/` branch naming scheme for hotfixes (`release/2024.07.15`).
- Deployments are triggered by merging a tag‑prefixed release to `main`; CI reads the tag to publish Docker images.
- Keep `docs/` and `CHANGELOG.md` in sync with code changes; the `code-reviewer` skill checklist includes a step to verify documentation updates.
