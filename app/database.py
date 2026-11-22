"""Small SQLAlchemy persistence layer: SQLite locally, PostgreSQL in Docker/K8s."""
import os
from datetime import date, datetime
from pathlib import Path

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Integer,
    String,
    Text,
    create_engine,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


def database_url() -> str:
    url = os.getenv("DATABASE_URL", "sqlite:///./data/tasks.db")
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://"):]
    return url


URL = database_url()
if URL.startswith("sqlite:///./"):
    Path(URL[len("sqlite:///./"):]).parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    URL,
    connect_args={"check_same_thread": False} if URL.startswith("sqlite") else {},
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class TaskRecord(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    priority: Mapped[str] = mapped_column(String(10), default="medium", nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
