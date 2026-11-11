
from fastapi.testclient import TestClient
from app.main import app, tasks

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_tasks():
    tasks.clear()

    # Create a new task
    response = client.post(
        "/tasks",
        json={"title": "Learn CI/CD"}
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Learn CI/CD"

    # Get all tasks
    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Learn CI/CD"

    tasks.clear()

def test_delete_task():
    tasks.clear()

    # Create a task
    response = client.post(
        "/tasks",
        json={"title": "Learn Docker"}
    )
    task_id = response.json()["id"]

    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Task deleted successfully"
    }

    # Check that deleting it again returns 404
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 404

    tasks.clear()

