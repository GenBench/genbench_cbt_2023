import json
from typing import Any, Dict, List, Mapping, Optional, Union

import numpy as np
from datasets import Dataset

from genbench import Task, TaskConfig
from genbench.api import DatasetSplit, EvaluationResult, PreparationStrategy, TaskType


def idx_to_ltr(idx):
    return chr(int(idx) + ord("A"))


def ltr_to_idx(ltr):
    return ord(ltr) - ord("A")


class OperationsresearchqaCot(Task):
    def __init__(
        self,
        config: TaskConfig,
        root_task_id: str,
        subtask_id: Optional[str] = None,
    ):
        self.reasoning_extraction = False
        super().__init__(config, root_task_id, subtask_id)

    def _format_example_for_in_context_learning(
        self, example: Mapping[str, Any], random_seed: int
    ) -> Mapping[str, Any]:
        """
        Format a given example for in-context learning.

        Parameters:
            example (Mapping[str, Any]): The input example to be formatted.
            random_seed (int): The random seed for any randomness in the formatting process.

        Returns:
            Mapping[str, Any]: A dictionary containing the formatted input and target.

        Raises:
            ValueError: If the specified task type is not supported.
        """
        prompt_config = self.config.preparation_strategies.prompt_based_testing.prompt_builder

        formatted_input = prompt_config.input_prefix + example["input"]

        if self.config.task_type == TaskType.MULTIPLE_CHOICE:
            choices = example["target_options"]

            # Append permuted choices to input if specified in config
            if prompt_config.append_choices_to_input:
                input_choices = choices[:]
                if prompt_config.permute_choices:
                    # Initialize a random number generator for handling permutations if needed
                    rng = np.random.RandomState(seed=random_seed + example["_genbench_idx"])
                    input_choices = rng.permutation(sorted(input_choices))

                formatted_input += prompt_config.choices_prefix + "".join(
                    [
                        f"{prompt_config.choice_item_prefix}{str(c)}{prompt_config.choice_item_postfix}"
                        for c in input_choices
                    ]
                )

            target = example["target"]

            formatted_input += prompt_config.output_prefix
            formatted_target = target

            return {
                "formatted_input": formatted_input,
                "formatted_target": formatted_target,
            }

        else:
            return super()._format_example_for_in_context_learning(example, random_seed)

    def evaluate_predictions(
        self, *, predictions: List[Mapping[str, Any]] = None, gold: Dataset = None
    ) -> EvaluationResult:
        refs_lst = [g["target"] for g in gold]
        ref_type = type(refs_lst[0])

        if ref_type == str:
            ref_options = set(refs_lst)
            if ref_options != {"A", "B", "C", "D"}:
                raise ValueError("The reference answer contains options that are not among A,B,C,D")

            gold = [{"target": ltr_to_idx(g["target"])} for g in gold]

        return super().evaluate_predictions(predictions=predictions, gold=gold)

    def get_prepared_datasets(
        self,
        preparation_strategy: PreparationStrategy,
        shot_list: Optional[List[int]] = None,
        reasoning_extraction: bool = False,
        random_seed: int = 42,
    ) -> Union[Mapping[DatasetSplit, Dataset], Mapping[int, Dataset]]:
        self.reasoning_extraction = reasoning_extraction

        prompt_builder = self.config.preparation_strategies.prompt_based_testing.prompt_builder

        instruction_index = 0 if reasoning_extraction else 1
        zeroshot_instruction = json.loads(prompt_builder.instruction_zero_shot)[instruction_index]
        fewshot_instruction = json.loads(prompt_builder.instruction_few_shot)[instruction_index]
        output_prefix = json.loads(prompt_builder.output_prefix)[instruction_index]
        few_shot_example_separator = json.loads(prompt_builder.few_shot_example_separator)[instruction_index]

        prompt_builder.instruction_zero_shot = zeroshot_instruction
        prompt_builder.instruction_few_shot = fewshot_instruction
        prompt_builder.output_prefix = output_prefix
        prompt_builder.few_shot_example_separator = few_shot_example_separator

        self.config.preparation_strategies.prompt_based_testing.prompt_builder = prompt_builder

        return super().get_prepared_datasets(preparation_strategy, shot_list, random_seed)

    def format_example(self, example: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform preprocessing/formatting on an example-level.
        Args:
            example: A dictionary containing key-value pairs for an example from the source dataset.
        Returns:
            A dictionary containing key-value pairs for the preprocessed/formatted example.
            The dictionary should contain keys `input` and `target`.
        """
        input_str = self.get_input_string(example)
        target_str = str(example["reasoning"]) if self.reasoning_extraction else str(idx_to_ltr(example["target"]))
        print(target_str)

        return {"input": input_str, "target": target_str, "target_options": {"A": 0, "B": 2, "C": 3, "D": 4}}

    def get_input_string(self, example: Dict[str, Any]):
        """
        A zero-shot example:
        Given the context (following Context:), select the most appropriate answer
        to the question (following Question:). Answer only 'A', 'B', 'C', or 'D'.
        Context: As a manager in an advertising agency, we are currently facing a
        media selection problem for one of our clients. Our client wants to place ads
        in various media to reach different demographic groups. Based on viewing and
        readership data, we have a table that shows the number of exposures obtained in each
        market segment per dollar spent on advertising in each medium. For each market segment,
        we have decided on a minimum desired number of exposures, as we believe that
        we must reach at least this number of readers or viewers, regardless of the cost.
        We also have a saturation level, which indicates that any exposure beyond this level
        is of no value to our client. Exposures between these two limits are considered useful
        exposures. Our objective is to determine how much should be spent on advertising in
        each medium, given an advertising budget and a target minimum of total useful exposures
        over all markets. The available media options include late-night TV, prime time TV,
        newspapers, billboards, and radio. We aim to maximize the overall impact of our client's
        advertising campaign while staying within budget and achieving the target minimum total useful exposures.
        Question: Which data parameters are participating in the objective criterion for this problem?
        A. Number of exposures achieved in a specific market segment per dollar spent on a specific media
        B. Total number of exposures achieved in each market segment
        C. Amount of money to be spent on advertising in each media channel
        D. None of the above
        Answer:

        """

        context_NL = example["context"]
        question_NL = example["question"]
        option_0 = example["target_options"][0]
        option_1 = example["target_options"][1]
        option_2 = example["target_options"][2]
        option_3 = example["target_options"][3]
        reasoning = example.get("reasoning", "{reasoning}")

        input_str = (
            "Context: "
            + str(context_NL)
            + "\nQuestion: "
            + str(question_NL)
            + "\nA. "
            + str(option_0)
            + "\nB. "
            + str(option_1)
            + "\nC. "
            + str(option_2)
            + "\nD. "
            + str(option_3)
        )

        if not self.reasoning_extraction:
            input_str = input_str + "\nReasoning: Let's think step by step " + reasoning

        return input_str
