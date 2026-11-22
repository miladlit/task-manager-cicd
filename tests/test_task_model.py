import pytest
from pydantic import ValidationError

from app.main import Task


def test_task_requires_title():
    with pytest.raises(ValidationError):
        Task()