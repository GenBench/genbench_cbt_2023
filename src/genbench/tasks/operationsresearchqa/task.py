from typing import Any, Dict

from genbench import Task


class OperationsresearchqaTask(Task):
    def format_example(self, example: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform preprocessing/formatting on an example-level.
        Args:
            example: A dictionary containing key-value pairs for an example from the source dataset.
        Returns:
            A dictionary containing key-value pairs for the preprocessed/formatted example.
            The dictionary should contain keys `input` and `target`.
        """
        context_NL = example["context"]
        question_NL = example["question"]
        option_0 = example["target_options"][0]
        option_1 = example["target_options"][1]
        option_2 = example["target_options"][2]
        option_3 = example["target_options"][3]
        target = example["target"]

        input_str = (
            "\nContext: "
            + str(context_NL)
            + "\nQuestion: "
            + str(question_NL)
            + "\nChoices:\n"
            + str(option_0)
            + "\n"
            + str(option_1)
            + "\n"
            + str(option_2)
            + "\n"
            + str(option_3)
        )
        target_str = str(target)

        return {
            "input": input_str,
            "target": target_str,
        }
