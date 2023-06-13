import os
from pathlib import Path
from typing import List

from genbench import tasks


def get_all_tasks_ids() -> List[str]:
    """Get all tasks slugs."""
    tasks_dir = Path(tasks.__file__).parent
    return list(
        [
            d.name
            for d in tasks_dir.iterdir()
            if d.is_dir() and not d.name.startswith("__")
        ]
    )


def get_task_dir(task_id: str) -> Path:
    """Get the path to the task directory."""
    tasks_dir = Path(tasks.__file__).parent
    return tasks_dir / task_id
