import importlib
import inspect
from pathlib import Path
from typing import Any, List, Mapping, Optional, Union

from genbench.task import Task
from genbench.task_config import TaskConfig
from genbench.task_dict import TaskDict
from genbench.utils.file import load_jsonnet
from genbench.utils.logging import get_logger
from genbench.utils.tasks import get_task_dir, get_task_module_name, is_task_dict


logger = get_logger(__name__)


def load_task(task_id: str) -> Union[Task, TaskDict]:
    """
    Loads a task by its ID, and optionally a subtask by its ID.

    Args:
        task_id (`str`): The identifier for the task. It can also include the subtask
        ID separated by a colon, e.g., 'task_id:subtask_id'.

    Returns:
        `Union[Task, TaskDict]`: An object representing the loaded task.
        It could be an instance of Task class or TaskDict depending on the task structure.

    Raises:
        ValueError: If the specified task does not exist.

    Notes:
        The function first checks if a subtask ID is provided (separated by ':').
        It then loads the task from the appropriate directory.
        If a subtask ID is provided, it tries to load the task as a Task class.
        If no subtask ID is provided, it checks if the directory points to a TaskDict,
        in which case it loads it as a TaskDict, otherwise it loads it as a Task class.
    """
    orig_task_id = task_id

    if ":" in task_id:
        task_id, subtask_id = task_id.split(":")
    else:
        subtask_id = None

    task_dir = get_task_dir(task_id, subtask_id=subtask_id)

    # Check if task exists
    if not task_dir.exists():
        raise ValueError(f"Task `{orig_task_id}` does not exist.")

    if subtask_id is not None:
        task_obj = _load_task_class(task_dir, task_id, subtask_id=subtask_id)
    else:
        # Check if task_dir points to a TaskDict
        if is_task_dict(task_dir):
            task_obj = _load_task_dict(task_dir, task_id)
        else:
            task_obj = _load_task_class(task_dir, task_id)

    return task_obj


def load_config(task_id: str) -> Union[TaskConfig, Mapping[str, Any]]:
    """
    Loads the configuration for a task by its ID, and optionally a subtask by its ID.

    Args:
        task_id (`str`): The identifier for the task.
        It can also include the subtask ID separated by a colon, e.g., 'task_id:subtask_id'.

    Returns:
        `Union[TaskConfig, Mapping[str, Any]]`: If a subtask ID is provided or the task directory doesn't point
        to a TaskDict, an instance of TaskConfig is returned.
        Otherwise, a dictionary mapping configuration keys to values is returned.

    Raises:
        ValueError: If the specified task does not exist.

    Notes:
        The function first checks if a subtask ID is provided (separated by ':').
        It then loads the task configuration from the appropriate directory.
        If a subtask ID is provided or the task directory doesn't point to a TaskDict,
        it loads the configuration as a TaskConfig.
        Otherwise, it loads the configuration as a dictionary.
    """
    orig_task_id = task_id

    if ":" in task_id:
        task_id, subtask_id = task_id.split(":")
    else:
        subtask_id = None

    task_dir = get_task_dir(task_id, subtask_id=subtask_id)

    # Check if task exists
    if not task_dir.exists():
        raise ValueError(f"Task `{orig_task_id}` does not exist.")

    if subtask_id is not None:
        return TaskConfig.from_jsonnet(jsonnet_path=task_dir / "config.jsonnet")
    else:
        # Check if task_dir points to a TaskDict
        if is_task_dict(task_dir):
            return load_jsonnet(task_dir / "config.jsonnet")
        else:
            return TaskConfig.from_jsonnet(jsonnet_path=task_dir / "config.jsonnet")


def _load_task_class(task_dir: Path, task_id: str, subtask_id: Optional[str] = None) -> Task:
    # Load task config
    config_path = task_dir / "config.jsonnet"
    config = TaskConfig.from_jsonnet(jsonnet_path=config_path)

    # Find task module
    task_module_name = f"{get_task_module_name(task_dir)}.task"

    # Import task module
    task_module = importlib.import_module(task_module_name)

    # Find task class
    task_class = None
    for name, obj in inspect.getmembers(task_module):
        if inspect.isclass(obj) and issubclass(obj, Task) and obj != Task:
            task_class = obj
            break

    if task_class is None:
        raise ValueError(f"Task `{task_id}` does not have a `Task` subclass.")

    task_obj = task_class(config, task_id, subtask_id=subtask_id)

    return task_obj


def _load_task_dict(task_dir: Path, task_id: str) -> TaskDict:
    # Load task dict config
    config_path = task_dir / "config.jsonnet"
    config = load_jsonnet(config_path)

    # Load TaskDict class
    task_dict_module_name = get_task_module_name(task_dir)
    task_dict_module = importlib.import_module(task_dict_module_name)
    task_dict_class = None
    for name, obj in inspect.getmembers(task_dict_module):
        if inspect.isclass(obj) and issubclass(obj, TaskDict) and obj != TaskDict:
            task_dict_class = obj
            break

    if task_dict_class is None:
        logger.info(f"`{task_id}.__init__.py` does not have a `TaskDict` subclass." f"Using default `TaskDict`.")
        task_dict_class = TaskDict

    # We load the subtasks in order specified in the config.
    # if the order is not specified, we load them in alphabetical order.
    subtask_ids: List[str] = config.get("subtasks_order", sorted([d.name for d in task_dir.iterdir()]))

    # Load subtasks
    subtasks_dict = {
        subtask_id: _load_task_class(task_dir / subtask_id, task_id, subtask_id=subtask_id)
        for subtask_id in subtask_ids
    }
    task_dict = task_dict_class.from_config(
        subtasks_dict=subtasks_dict,
        config=config,
        task_id=task_id,
    )

    return task_dict
