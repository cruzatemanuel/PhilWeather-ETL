---
name: docker-engineer
description: Provides guidelines for containerising Python ETL, Airflow, and dbt services for the PhilWeather project.
---

# Purpose
Standardise Docker image creation, multi‑stage builds, and orchestration for reliable deployment of the weather ETL stack.

# When to Use
- Building a reproducible environment for the ETL loader, Airflow scheduler, and dbt runner.
- Creating a CI/CD pipeline that pushes images to a registry.
- Optimising image size for fast start‑up in Kubernetes or Docker Swarm.
- Managing Secrets and environment variables at runtime.

# Responsibilities
- Write `Dockerfile`s with multi‑stage builds.
- Define `docker-compose.yml` for local development.
- Configure health‑checks and resource limits.
- Publish images to a container registry (GitHub Packages, Docker Hub).
- Provide troubleshooting guide for common container issues.

# Workflow
1. **Base Image Selection** – Use official `python:3.12-slim` for runtime; `python:3.12` for build stage.
2. **Dependency Layer** – Install system packages (`libpq-dev`, `gcc`) in the build stage, copy `requirements.txt`, run `pip install --no-cache-dir`.
3. **Copy Source** – Transfer only necessary package files (`src/`, `pyproject.toml`).
4. **Entry Point** – Use `ENTRYPOINT ["python", "-m", "philweather_etl"]` or appropriate Airflow command.
5. **Testing Locally** – Run `docker compose up --build` and execute integration tests against the containers.
6. **CI Integration** – In GitHub Actions, build image, run `docker run --rm` smoke tests, then push with semantic tags.
7. **Production Deploy** – Deploy via Helm chart or Docker Swarm, set `restart: on-failure` and resource limits.

# Best Practices
- Keep layers immutable; order `apt-get` before `pip install` to leverage caching.
- Use `USER nonroot` with UID/GID 1000 to avoid root inside container.
- Pin exact versions of base images and dependencies.
- Store secrets in environment variables via Docker secrets or Kubernetes secrets – never bake them into the image.
- Leverage `docker healthcheck` to verify service readiness (e.g., `curl -f http://localhost:8080/health`).

# Anti‑patterns
- Installing unnecessary development tools (`git`, `vim`) in the final image.
- Copying the entire repository (`COPY . .`) leading to large image size.
- Using `latest` tag for base images – leads to non‑reproducible builds.
- Running containers with `--privileged` unless absolutely required.
- Hard‑coding credentials in Dockerfile `ENV` statements.

# Checklist
- [ ] `Dockerfile` builds without errors (`docker build .`).
- [ ] Image size < 200 MB.
- [ ] Multi‑stage build separates build and runtime layers.
- [ ] Health check defined and passes locally.
- [ ] CI pipeline runs `docker compose up -d` and executes integration test suite.
- [ ] Image pushed to `ghcr.io/<org>/philweather-loader` with semantic version tag.

# Examples
```Dockerfile
# ---------- Build Stage ----------
FROM python:3.12-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip && pip install poetry && poetry export -f requirements.txt --output requirements.txt --without-hashes
COPY src/ ./src/
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Runtime Stage ----------
FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app/src ./src
ENV PYTHONPATH=/app/src
USER 1000:1000
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s CMD curl -f http://localhost:8080/health || exit 1
ENTRYPOINT ["python", "-m", "philweather_etl.loader"]
```

# Project‑Specific Guidance
- Use the `docker/loader/` directory for the ETL loader image and `docker/airflow/` for Airflow compose files.
- Tag images with the Git commit SHA (`philweather/loader:${GIT_SHA}`).
- Store Supabase credentials in Docker secrets and mount them in the containers (`/run/secrets/supabase_key`).
- After dbt runs, trigger Metabase refresh via a lightweight `alpine` container that calls the Metabase API.
