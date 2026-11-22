# TaskFlow — Task Manager + DevOps Practice

This started as my CI/CD course project at Nackademin. I improved it to practise the tools used in real DevOps work, especially for my upcoming LIA.

The app is a FastAPI task manager with a modern website, PostgreSQL support, automatic tests, Docker, Prometheus metrics and a GitHub Actions pipeline.

## Features

- Modern dashboard at **http://localhost:8000/dashboard**
- Add, edit, complete and delete tasks
- Task priorities, descriptions and due dates
- Search and filter tasks, plus progress statistics
- Data stored in SQLite locally or PostgreSQL with Docker Compose
- API docs at **http://localhost:8000/docs**
- Health check `/health`, database readiness `/ready`, Prometheus metrics `/metrics`

## Run locally (Python)

```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The app creates `data/tasks.db` automatically. This is ignored by Git. Open **http://localhost:8000/dashboard**.

## Run with PostgreSQL and Docker

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
```

This starts the app and a PostgreSQL database. Open **http://localhost:8000/dashboard**. Tasks are saved in a named Docker volume.

Stop containers without deleting data: `docker compose down`

**Do not use `docker compose down -v` unless you want to delete the PostgreSQL data.**

## Tests

```bash
python -m pytest -v
python -m ruff check app tests
```

There are unit tests for the task model and a pure summary function, and integration tests for the API. Tests use an isolated in-memory SQLite database, so they don't change your own tasks.

## CI/CD

A push/PR runs Pytest and Ruff. If they pass, the pipeline builds Docker and checks `/health`, `/ready` and the dashboard. Test results are saved as a downloadable artifact.

On a push to `main`, the pipeline also publishes a Docker image to GHCR, tagged with the commit SHA and `latest`.

If a repository secret named `INFRA_REPO_TOKEN` exists, another job updates the image tag in `miladlit/task-manager-infrastructure`. Argo CD can then deploy it to Kubernetes. If the secret is not set, that update is skipped.

**Important:** GHCR images may initially be private; make the practice package public or configure a Kubernetes pull secret. The first tag has to be published before Kubernetes can pull it.

## Infrastructure and monitoring

The companion repo is called `task-manager-infrastructure`. It contains Kubernetes, Argo CD, Prometheus, Grafana and optional OpenStack Terraform training files. Read its README first.

## Old rollback demo

The original `scripts/deploy_local.sh`, `scripts/verify.sh` and `scripts/rollback_local.sh` were kept for the **old v1/v2 images**. They are a separate demonstration and do not deploy the new TaskFlow v3 image. See `docs/PRESENTATION.md`.

## Limitations

- This is a learning environment, not a production cloud service.
- SQLite is for one local instance; Kubernetes uses shared PostgreSQL.
- Database table creation uses SQLAlchemy `create_all`; a real team should use migrations (e.g., Alembic).
- PostgreSQL in the training Kubernetes cluster has one instance and no backups or high availability.
- The website does not have user accounts or authentication. Don't expose it publicly with real data.
- A real deployment should include secret management, TLS, access controls, backups and security scanning.

## What I learned

CI/CD is about getting early feedback and releasing working changes safely. The project now also helps me practise database persistence, Kubernetes, GitOps and observability.
