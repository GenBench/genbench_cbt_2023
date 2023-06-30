import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Optional, Union

from .file import get_repo_dir


def get_all_tasks_ids() -> List[str]:
    from genbench import tasks

    """Get all tasks slugs."""
    tasks_dir = Path(tasks.__file__).parent
    return list(
        [
            d.name
            for d in tasks_dir.iterdir()
            if d.is_dir() and not d.name.startswith("__") and is_valid_task_id(d.name)
        ]
    )


def get_all_tasks_and_subtasks_ids() -> List[str]:
    """Get all tasks and subtasks slugs."""
    task_ids = []
    for task_id in get_all_tasks_ids():
        task_dir = get_task_dir(task_id)
        if is_task_dict(task_dir):
            task_ids.append(task_id)
            task_ids.extend(
                [f"{task_id}:{s}" for s in get_task_dict_subtasks(task_dir)]
            )
        else:
            task_ids.append(task_id)
    return task_ids


def get_tasks_dir() -> Path:
    """Get the path to the `tasks` directory."""
    from genbench import tasks

    tasks_dir = Path(tasks.__file__).parent
    return tasks_dir


def get_task_dir(task_id: str, subtask_id: Optional[str] = None) -> Path:
    """Get the path to the task directory."""
    if ":" in task_id:
        task_id, subtask_id = task_id.split(":")

    tasks_dir = get_tasks_dir()
    if subtask_id is not None:
        return tasks_dir / task_id / subtask_id
    else:
        return tasks_dir / task_id


def get_task_module_name(task_dir: Path) -> str:
    """Get the name of the task module from the task directory."""
    import genbench

    start_path = Path(genbench.__file__).parent
    rel_task_dir = task_dir.relative_to(start_path)
    task_module_name = f"genbench.{rel_task_dir.as_posix().replace('/', '.')}"
    return task_module_name


def is_valid_task_id(id_: str) -> bool:
    """Check if a task id is valid."""
    return all(
        (c.isalnum() and ord(c) < 128 and c.lower() == c) or c == "_" for c in id_
    )


def is_valid_task_module(task_dir: Path) -> bool:
    """Check if a task module is valid."""
    return all(
        [
            (task_dir / "__init__.py").exists(),
            (task_dir / "task.py").exists(),
            (task_dir / "config.jsonnet").exists(),
        ]
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

    from genbench import TaskDict

    # Load the module and check if it has a TaskDict class
    task_dict_module_name = get_task_module_name(task_dir)
    task_dict_module = importlib.import_module(task_dict_module_name)
    for name, obj in inspect.getmembers(task_dict_module):
        if inspect.isclass(obj) and issubclass(obj, TaskDict) and obj != TaskDict:
            return True

    return False


def get_task_dict_subtasks(task_dir: Path) -> List[str]:
    """Get the subtasks of a task dict based on the task directory."""
    return sorted(
        [
            d.name
            for d in task_dir.iterdir()
            if d.is_dir()
            and not d.name.startswith("__")
            and is_valid_task_id(d.name)
            and is_valid_task_module(d)
        ]
    )


def get_all_task_metadata() -> Dict[str, Union[str, Dict[str, str]]]:
    """Get metadata for all tasks."""
    from genbench import TaskDict
    from genbench.loading import load_task

    task_ids = get_all_tasks_ids()
    task_metadata = {}
    for task_id in task_ids:
        task = load_task(task_id)
        metadata = {
            "name": task.name,
            "description": task.description,
            "keywords": task.keywords,
            "authors": task.authors,
        }
        if isinstance(task, TaskDict):
            metadata["subtasks"] = {}
            for subtask_id, subtask in task.items():
                metadata["subtasks"][subtask_id] = {
                    "name": subtask.name,
                    "description": subtask.description,
                    "keywords": subtask.keywords,
                    "authors": subtask.authors,
                }

        task_metadata[task_id] = metadata

    return task_metadata
