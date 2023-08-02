from genbench import Task
from typing import Any, Dict


class BiasAmplifiedSplitsMnli(Task):
    def format_example(self, example: Dict[str, Any]) -> Dict[str, Any]:
        """Perform preprocessing/formatting on an example-level.

        By default, this method does nothing more than mapping original data source
        fields to the expected fields.

        `example` directly comes from the data source (e.g. downloaded HF dataset),
        and it may contain fields such as `question` or `answer`. This method should
        prepare the example used in the task. i.e. should create fields `input`,
        `target`, `target_scores`, or `target_labels` depending on the task type.

        Args:
            example: A dictionary containing key-value pairs for an example from the source dataset.


        Returns:
            A dictionary containing key-value pairs for the preprocessed/formatted example.
            The dictionary should contain keys `input`, `target`, `target_scores`, or `target_label`
            depending on the task type.
        """
        return {
            "input": f"{example['premise']} </s> {example['hypothesis']}",
            "target": example["label"],
        }
