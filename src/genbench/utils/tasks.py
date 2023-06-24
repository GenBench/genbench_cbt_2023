import importlib
import inspect
from pathlib import Path
from typing import List, Optional, Dict, Union

import genbench
from genbench import tasks
from genbench.task_dict import TaskDict
from genbench.utils.file import get_repo_dir


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


def get_tasks_dir() -> Path:
    """Get the path to the `tasks` directory."""
    tasks_dir = Path(tasks.__file__).parent
    return tasks_dir


def get_task_dir(task_id: str, subtask_id: Optional[str] = None) -> Path:
    """Get the path to the task directory."""
    tasks_dir = Path(tasks.__file__).parent
    if subtask_id is not None:
        return tasks_dir / task_id / subtask_id
    else:
        return tasks_dir / task_id


def get_task_module_name(task_dir: Path) -> str:
    """Get the name of the task module from the task directory."""
    start_path = Path(genbench.__file__).parent
    rel_task_dir = task_dir.relative_to(start_path)
    task_module_name = f"genbench.{rel_task_dir.as_posix().replace('/', '.')}"
    return task_module_name


def is_valid_task_id(id_: str) -> bool:
    """Check if a task id is valid."""
    return all(
        (c.isalnum() and ord(c) < 128 and c.lower() == c) or c == "_" for c in id_
    )


def generate_task_from_template(
    name: str,
    task_id: str,
    task_class_name: str,
    task_authors: List[str],
    output_dir: Optional[Path] = None,
) -> None:
    """Create a task from a template using cookiecutter"""
    from cookiecutter.main import cookiecutter

    if output_dir is None:
        output_dir = get_tasks_dir()

    cookiecutter(
        str(get_repo_dir() / "templates" / "task"),
        extra_context={
            "task_name": name,
            "task_id": task_id,
            "task_class_name": task_class_name,
            "task_authors": task_authors,
        },
        output_dir=str(output_dir),
        overwrite_if_exists=True,
        no_input=True,
    )


def is_task_dict(task_dir: Path) -> bool:
    if (task_dir / "task.py").exists():
        return False

    # Load the module and check if it has a TaskDict class
    task_dict_module_name = get_task_module_name(task_dir)
    task_dict_module = importlib.import_module(task_dict_module_name)
    for name, obj in inspect.getmembers(task_dict_module):
        if inspect.isclass(obj) and issubclass(obj, TaskDict) and obj != TaskDict:
            return True

    return False


def get_all_task_metadata() -> Dict[str, Union[str, Dict[str, str]]]:
    """Get metadata for all tasks."""
    from genbench.loading import load_task

    task_ids = get_all_tasks_ids()
    task_metadata = {}
    for task_id in task_ids:
        task = load_task(task_id)
        metadata = {
            "name": task.config.name,
            "description": task.config.description,
            "keywords": task.config.keywords,
            "authors": task.config.authors,
        }
        if isinstance(task, TaskDict):
            metadata["subtasks"] = {}
            for subtask_id, subtask in task.items():
                metadata["subtasks"][subtask_id] = {
                    "name": subtask.config.name,
                    "description": subtask.config.description,
                    "keywords": subtask.config.keywords,
                    "authors": subtask.config.authors,
                }

        task_metadata[task_id] = metadata

    return task_metadata
