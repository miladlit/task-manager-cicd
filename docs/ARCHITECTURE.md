# TaskFlow architecture (simple)

```text
                APP REPOSITORY
       Developer changes code in Git
                    |
                    v
       GitHub Actions: Pytest + Ruff
                    |
                    v
       Build Docker + /health + /ready
                    |
                    v
          Publish image to GHCR
                    |
          optional token update
                    v
             INFRA REPOSITORY
       k8s/app.yaml points to image
                    |
             Argo CD watches Git
                    |
                    v
      Kubernetes deploys TaskFlow Pod
                    |
           FastAPI  <----> PostgreSQL
                    |
                  /metrics
                    |
               Prometheus
                    |
                 Grafana
```

**Local development:** SQLite is used by default. `docker compose up` starts PostgreSQL plus the web app. GitHub Actions' Docker test uses a temporary SQLite-backed app, not a production server.

**Deployment:** Argo CD reads the infrastructure repo and asks Kubernetes to run the selected image. Kubernetes readiness checks database access. GHCR must be accessible to the cluster.

**Rollback:** old Docker tags support the earlier v1/v2 course demonstration. In GitOps, revert the image tag in Git; a manual `kubectl rollout undo` may be overwritten by Argo CD's automatic sync.

**OpenStack:** a separate infrastructure layer that can host VMs/clusters, if you have actual cloud access. No OpenStack resources are created by the application pipeline.
