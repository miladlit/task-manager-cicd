"""API integration tests. The original endpoints still work."""


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_tasks(client):
    response = client.post("/tasks", json={"title": "Learn CI/CD"})
    assert response.status_code == 200
    assert response.json()["title"] == "Learn CI/CD"

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Learn CI/CD"


def test_delete_task(client):
    response = client.post("/tasks", json={"title": "Learn Docker"})
    task_id = response.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}
    assert client.delete(f"/tasks/{task_id}").status_code == 404


def test_update_task_and_stats(client):
    task = client.post("/tasks", json={"title": "Learn Kubernetes"}).json()
    updated = client.patch(
        f"/tasks/{task['id']}", json={"completed": True, "priority": "high"}
    )
    assert updated.status_code == 200
    assert updated.json()["completed"] is True
    assert updated.json()["priority"] == "high"
    assert client.get("/stats").json() == {"total": 1, "completed": 1, "remaining": 0}


def test_ids_do_not_repeat_after_delete(client):
    a = client.post("/tasks", json={"title": "First"}).json()
    b = client.post("/tasks", json={"title": "Second"}).json()
    client.delete(f"/tasks/{a['id']}")
    c = client.post("/tasks", json={"title": "Third"}).json()
    assert len({a["id"], b["id"], c["id"]}) == 3


def test_dashboard_and_metrics(client):
    assert client.get("/dashboard").status_code == 200
    assert "text/html" in client.get("/dashboard").headers["content-type"]
    assert client.get("/ready").json() == {"status": "ready"}
    assert b"taskflow_http_requests_total" in client.get("/metrics").content

def test_homepage_redirects_to_dashboard(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/dashboard"

def test_version_for_demo(client):
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "3.0"}

                               
                                
