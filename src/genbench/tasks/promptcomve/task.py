from typing import Any, Dict

from genbench import Task


class PromptcomveTask(Task):
    def format_example(self, example: Dict[str, Any]) -> Dict[str, Any]:
        return {"input": example["prompt"], "target": example["target"]}
