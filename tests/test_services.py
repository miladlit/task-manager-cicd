"""Pure unit tests without database or API."""
from dataclasses import dataclass

from app.services import task_summary


@dataclass
class ExampleTask:
    completed: bool


def test_task_summary_counts_completed_and_remaining():
    tasks = [ExampleTask(False), ExampleTask(True), ExampleTask(False)]
    assert task_summary(tasks) == {"total": 3, "completed": 1, "remaining": 2}


def test_task_summary_handles_empty_list():
    assert task_summary([]) == {"total": 0, "completed": 0, "remaining": 0}
