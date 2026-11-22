# TaskFlow presentation and live demo (5–8 minutes)

**Important:** Only demonstrate or claim a step as complete if it actually works on your own laptop/GitHub.

## Talking points (simple English)

**1. Intro (30 seconds)**

"This is TaskFlow, my Task Manager project. I started it to learn CI/CD. Then I improved it to practise real DevOps tools before my internship."

**2. App demonstration (1 minute)**

Open `http://localhost:8000/dashboard`. Create a task called "Learn Kubernetes", set high priority, complete it and show the progress counter. Refresh the website to show database persistence.

**3. Testing (1 minute)**

Open tests in VS Code. Run `python -m pytest -v` and `python -m ruff check app tests`.

"Unit tests check small pieces of logic. Integration tests check how the API endpoints work together with the database. The pipeline stops if tests fail."

**4. CI/CD (1 minute)**

Open the GitHub Actions page for your app repo. Show a successful run. Explain the `test` job, `docker-build` job, artifact, and publishing to GHCR *only if enabled and passing*. Show the previous intentionally failed test PR if you still have the run.

"I designed the pipeline so the Docker job only runs after tests pass. The health and readiness checks verify that the application can actually respond."

**5. Containers and GitOps (1–2 minutes)**

Explain: "GitHub Actions tests and publishes an image. The infrastructure repository stores Kubernetes configuration. Argo CD watches the repository and applies changes to the cluster." If deployed, run `kubectl get pods -n taskflow` and show Argo CD. Otherwise explain it as the next step, not a completed deployment.

**6. Monitoring (30 seconds)**

If running, show Grafana at `http://localhost:3000` and Prometheus at `http://localhost:9090/targets`. Mention request count, error count, and latency.

**7. Rollback and limits (1 minute)**

Show the legacy v1/v2 local rollback if the old images exist. Or show `kubectl rollout history deployment/taskflow -n taskflow` for Kubernetes once versions have changed.

"A rollback returns to a previous working version. My environment is still a practice setup: it needs proper security, backups, and production-grade operations."

## Evidence/screenshots to prepare

1. The website with tasks visible.
2. Passing pytest and Ruff terminal output.
3. GitHub Actions successful test + Docker jobs and artifact.
4. Previous failed-run log showing that a test blocked the Docker job.
5. Docker Compose containers and PostgreSQL persistence.
6. `kubectl get pods -n taskflow`, Argo CD UI and Grafana dashboard **if actually deployed**.

## Quick demo commands

```bash
python -m pytest -v
python -m ruff check app tests
docker compose ps
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl http://localhost:8000/version
```

For Kubernetes (only if configured):

```bash
kubectl get pods -n taskflow
kubectl get services -n taskflow
kubectl rollout status deployment/taskflow -n taskflow
```

## Questions the teacher might ask

- **Why unit tests and integration tests?** They catch different kinds of problems.
- **Why run tests before Docker?** Avoid building and publishing broken versions.
- **Why Docker?** Package the app consistently in different environments.
- **Why two Git repos?** Separate app development from infrastructure and GitOps.
- **Why PostgreSQL instead of just a list?** Tasks persist after restart; replicas share one database.
- **Why readiness and liveness?** Liveness shows the process responds; readiness checks database connectivity.
- **Why Argo CD?** It makes the deployed environment match Git configuration.
- **Why Prometheus/Grafana?** Metrics help spot errors and performance problems.
- **What would you improve?** Authentication, database migrations, security scanning, backups and production monitoring.
