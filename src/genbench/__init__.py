from .loading import load_config, load_task
from .task import Task
from .task_config import TaskConfig
from .task_dict import TaskDict
from .utils import logging as genbench_logging


genbench_logging.enable_default_handler()
genbench_logging.enable_explicit_format()
