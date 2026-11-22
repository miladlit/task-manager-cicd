"""Pure functions that are easy to unit test."""


def task_summary(tasks: list[object]) -> dict[str, int]:
    """Calculate task counts from objects that have a completed attribute."""
    total = len(tasks)
    completed = sum(bool(task.completed) for task in tasks)
    return {"total": total, "completed": completed, "remaining": total - completed}
