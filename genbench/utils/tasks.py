import os
from pathlib import Path
from typing import List

from genbench import tasks


def get_all_tasks_slugs() -> List[str]:
    """Get all tasks slugs."""
    tasks_dir = Path(tasks.__file__).parent
    return list(
        [
            d.name
            for d in tasks_dir.iterdir()
            if d.is_dir() and not d.name.startswith("__")
        ]
    )
