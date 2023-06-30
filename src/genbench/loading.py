import importlib
import inspect
from pathlib import Path
from typing import List, Optional, Union

from genbench.task import Task
from genbench.task_config import TaskConfig
from genbench.task_dict import TaskDict
from genbench.utils.file import load_jsonnet
from genbench.utils.logging import get_logger
from genbench.utils.tasks import get_task_dir, get_task_module_name, is_task_dict


logger = get_logger(__name__)


def load_task(task_id: str) -> Union[Task, TaskDict]:
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
