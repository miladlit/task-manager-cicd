"""Model unit tests (no HTTP request needed)."""
import pytest
from pydantic import ValidationError

from app.main import Task


def test_task_requires_title():
    with pytest.raises(ValidationError):
        Task()


def test_blank_title_is_rejected():
    with pytest.raises(ValidationError):
        Task(title="  ")


def test_title_is_trimmed():
    assert Task(title="   Learn OpenStack   ").title == "Learn OpenStack"
