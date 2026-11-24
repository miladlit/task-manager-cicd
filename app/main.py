"""TaskFlow API and dashboard. Preserves the original API endpoints."""
from contextlib import asynccontextmanager
from datetime import date, datetime
from pathlib import Path
from time import perf_counter
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.database import TaskRecord, get_db, init_db
from app.services import task_summary

STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="TaskFlow API", version="3.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

REQUESTS = Counter(
    "taskflow_http_requests_total", "Total HTTP requests", ["method", "route", "status"]
)
DURATION = Histogram(
    "taskflow_http_request_duration_seconds", "HTTP request duration", ["method", "route"]
)


@app.middleware("http")
async def record_metrics(request: Request, call_next):
    start = perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        REQUESTS.labels(request.method, "exception", "500").inc()
        raise
    route = request.scope.get("route")
    route_name = route.path if route is not None else "unknown"
    if route_name != "/metrics":
        REQUESTS.labels(request.method, route_name, str(response.status_code)).inc()
        DURATION.labels(request.method, route_name).observe(perf_counter() - start)
    return response


class Task(BaseModel):
    """Request model kept under its original name for earlier unit tests."""

    title: str = Field(min_length=1, max_length=150)
    description: str = Field(default="", max_length=2000)
    priority: Literal["low", "medium", "high"] = "medium"
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Task title cannot be empty")
        return value


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    priority: Literal["low", "medium", "high"] | None = None
    completed: bool | None = None
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("Task title cannot be empty")
        return value


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    priority: str
    completed: bool
    due_date: date | None
    created_at: datetime


@app.get("/")
def home():
    return RedirectResponse(url="/dashboard")


@app.get("/dashboard", include_in_schema=False)
def dashboard():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready(db: Annotated[Session, Depends(get_db)]):
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Database is not ready") from exc
    return {"status": "ready"}


@app.get("/version")
def get_version():
    return {"version": "3.0", "message": "TaskFlow Dashboard Version 3"}


@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Annotated[Session, Depends(get_db)]):
    return db.scalars(select(TaskRecord).order_by(TaskRecord.id.desc())).all()


@app.post("/tasks", response_model=TaskResponse)
def create_task(task: Task, db: Annotated[Session, Depends(get_db)]):
    record = TaskRecord(**task.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Annotated[Session, Depends(get_db)]):
    record = db.get(TaskRecord, task_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    record = db.get(TaskRecord, task_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(record)
    db.commit()
    return {"message": "Task deleted successfully"}


@app.get("/stats")
def stats(db: Annotated[Session, Depends(get_db)]):
    records = db.scalars(select(TaskRecord)).all()
    return task_summary(records)
