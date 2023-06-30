from collections import OrderedDict
from typing import Mapping, Any, List

from genbench.api import EvaluationResult
from genbench.task import Task
from genbench.utils.logging import get_logger

logger = get_logger(__name__)


class TaskDict(OrderedDict, Mapping[str, Task]):
    """A TaskDict is a task with subtasks."""

    @classmethod
    def from_config(cls, subtasks_dict: dict, config: Mapping[str, Any], task_id: str) -> "TaskDict":
        """Construct a TaskDict from a config dict."""
        obj = cls(subtasks_dict)
        obj._config = config
        obj._task_id = task_id

        return obj

    @property
    def name(self) -> str:
        return self._config["name"]

    @property
    def task_id(self) -> str:
        return self._task_id

    @property
    def keywords(self) -> List[str]:
        """
        TaskDict's list of keywords.

        If config["keywords"] is a list, return it. Otherwise, we read the keywords
        from subtasks and return the union of all keywords in the order of subtasks.
        """
        if "keywords" in self._config and isinstance(self._config["keywords"], list):
            return self._config["keywords"]
        else:
            self._check_values_type()
            keywords = []
            for task in self.values():
                task_keywords = task.config.keywords
                for keyword in task_keywords:
                    if keyword not in keywords:
                        keywords.append(keyword)
            return keywords

    @property
    def authors(self) -> List[str]:
        """
        TaskDict's list of authors.

        If config["authors"] is a list, return it. Otherwise, we read the authors
        from subtasks and return the union of all authors in the order of subtasks.
        """
        if "authors" in self._config and isinstance(self._config["authors"], list):
            return self._config["authors"]
        else:
            self._check_values_type()
            authors = []
            for task in self.values():
                task_authors = task.config.authors
                for author in task_authors:
                    if author not in authors:
                        authors.append(author)
            return authors

    @property
    def description(self) -> str:
        """
        TaskDict's description. A general description of the task.

        If config["description"] provided, return it. Otherwise, we read the
        descriptions from subtasks and compile them into a single description
        using a template.
        """
        if "description" in self._config and isinstance(self._config["description"], str):
            return self._config["description"]
        else:
            self._check_values_type()
            descriptions = []
            for task in self.values():
                task_description = task.config.description
                # Add subtask name and id to the description
                task_description = f"## {task.name} ({task.subtask_id})\n{task_description}"
                descriptions.append(task_description)
            return "\n\n".join(descriptions)

    def merge_evaluation_results(self, results: OrderedDict[str, EvaluationResult]) -> EvaluationResult:
        """Merge evaluation results from subtasks.

        The default implementation is to merge the results into a single
        EvaluationResult object, where keys are prefixed with subtask ids.

        Args:
            results (OrderedDict[str, EvaluationResult]): Evaluation results from subtasks.

        Returns:
            EvaluationResult: Merged evaluation results.
        """
        self._check_values_type()
        merged_results = EvaluationResult()
        for subtask_id, result in results.items():
            for metric, value in result.items():
                merged_results[f"{subtask_id}.{metric}"] = value
        return merged_results

    def _check_values_type(self):
        for task in self.values():
            if not isinstance(task, Task):
                raise TypeError(f"Expected value of type `Task` but got {type(task)} instead.")

    def __getitem__(self, k) -> Task:
        return super().__getitem__(k)

    # Allow item access by attribute
    def __getattr__(self, k) -> Task:
        if isinstance(k, str) and not k.startswith("_"):
            return self[k]
        else:
            return super().__getattr__(k)
