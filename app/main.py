
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task Manager API")

tasks = []


class Task(BaseModel):
    title: str


@app.get("/")
def home():
    return {"message": "Welcome to Task Manager API"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks")
def create_task(task: Task):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title
    }
    tasks.append(new_task)
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}

    raise HTTPException(status_code=404, detail="Task not found")

