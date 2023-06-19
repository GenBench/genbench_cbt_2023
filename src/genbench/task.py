from typing import Optional, Mapping, List, Any, Union, Callable

import evaluate
import numpy as np
from datasets import (
    IterableDataset,
    IterableDatasetDict,
    Dataset,
    DatasetDict,
    load_dataset,
)

from genbench import TaskConfig
from genbench.api import TaskInterface, DatasetSplit, TaskType, PreparationStrategy
from genbench.task_config import PromptBuilderConfig
from genbench.utils.file import load_jsonnet
from genbench.utils.logging import get_logger

logger = get_logger(__name__)


def get_data_split_name(split: str) -> str:
    """
    Transforms the name of a data split for standardization purposes.

    This function converts 'dev' splits to 'validation' in the dataset split name and removes the file extension.
    It's useful for standardizing dataset split names when working with datasets that have different naming conventions.

    Args:
        split (str): The original name of the data split.

    Returns:
        str: The standardized name of the data split.
    """
    if "dev" in split:
        return split.replace("dev", "validation").replace(".tsv", "")
    else:
        return split.split(".")[0]


def resplit_data_source(
    orig_datasets: DatasetDict, splitting_info: Mapping[str, List[str]]
) -> DatasetDict:
    """
    Resplits an original dataset according to provided split information.

    This function asserts that all keys in split_info are present in the original datasets,
    then generates a new DatasetDict with resplit data. It uses the same features as the original dataset
    for each new split.

    Args:
        orig_datasets (DatasetDict): The original dataset to be split.
        splitting_info (Mapping[str, List[str]]): A mapping that defines how to split the original dataset.
            Each key is a split name, and its corresponding value is a list of identifiers in the format 'orig_split:orig_id'.

    Raises:
        AssertionError: If there are keys in split_info that are not in the original dataset.

    Returns:
        DatasetDict: A new dictionary of datasets where each dataset corresponds to a split defined in split_info.

    """
    assert set(splitting_info.keys()).issubset(set(orig_datasets.keys())), (
        f"Split info contains keys {set(orig_datasets.keys()) - set(splitting_info.keys())} "
        f"that are not in the original dataset "
    )

    def get_generator_fn(split_name: str):
        def generator_fn():
            for sid in splitting_info[split_name]:
                orig_split, orig_id = sid.split(":")
                orig_split = orig_split.split(".")[0]
                orig_split = get_data_split_name(orig_split)
                yield from orig_datasets[orig_split][int(orig_id)]

        return generator_fn

    return DatasetDict(
        {
            split_name: Dataset.from_generator(
                get_generator_fn(split_name),
                features=orig_datasets[split_name].features,
            )
            for split_name in sorted(splitting_info.keys())
        }
    )


def make_nshot_dataset(
    formatted_dataset: Mapping[DatasetSplit, Dataset],
    prompt_builder_config: PromptBuilderConfig,
    shot_formatter: Callable[[Mapping[str, Any], int], Mapping[str, Any]],
    num_shots: int,
    random_seed: int,
    repeat_samples: int = 1,
    num_proc: int = 4,
) -> Dataset:
    test_set = formatted_dataset[DatasetSplit.TEST]
    assert (
        test_set is not None
    ), "Test set is required for creating fewshot-shot dataset"

    if num_shots == 0:

        def create_zeroshot_example(example):
            formatted_example = shot_formatter(example, random_seed)
            formatted_input = formatted_example["formatted_input"]
            formatted_target = formatted_example["formatted_target"]

            assert isinstance(formatted_input, str)
            assert isinstance(formatted_target, str)

            formatted_input = prompt_builder_config.instruction + formatted_input

            return {
                "input": formatted_input,
                "target": formatted_target,
                "original_input": example["input"],
                "original_target": example["target"],
            }

        test_set.map(
            create_zeroshot_example,
            num_proc=num_proc,
            desc="Converting test set to n-shot format",
        )

        return test_set

    if DatasetSplit.TRAIN in formatted_dataset:
        fewshot_example_source = formatted_dataset[DatasetSplit.TRAIN]
    elif DatasetSplit.VALIDATION in formatted_dataset:
        fewshot_example_source = formatted_dataset[DatasetSplit.VALIDATION]
        logger.warning("Using validation set as few-shot example source.")
    else:
        fewshot_example_source = formatted_dataset[DatasetSplit.TEST]
        logger.warning("Using test set as few-shot example source.")

    if len(fewshot_example_source) < num_shots + 1:
        raise ValueError("Not enough examples for the number of shots.")

    formatted_test_set = test_set.map(
        lambda example: shot_formatter(example, random_seed),
        num_proc=num_proc,
        desc="Formatting test set for few-shot dataset creation",
    )

    queries = formatted_test_set
    if repeat_samples != 1:

        def repeat_examples(
            example_dict: Mapping[str, List[Any]]
        ) -> Mapping[str, List[Any]]:
            return {
                key: [value] * repeat_samples for key, value in example_dict.items()
            }

        queries = formatted_test_set.map(
            repeat_examples,
            num_proc=num_proc,
            batched=True,
        )

    def create_fewshot_query(query, idx):
        rng = np.random.RandomState(random_seed + idx)

        in_context_example_ids = rng.choice(
            len(fewshot_example_source), num_shots, replace=False
        )
        in_context_examples = [
            fewshot_example_source[i]
            for i in in_context_example_ids
            if fewshot_example_source[i] != query
        ]

        context = prompt_builder_config.few_shot_example_separator.join(
            [
                example["formatted_input"] + example["formatted_target"]
                for example in in_context_examples
            ]
        )

        formatted_input = (
            prompt_builder_config.instruction + context + query["formatted_input"]
        )
        formatted_target = query["formatted_target"]

        return {
            "input": formatted_input,
            "target": formatted_target,
            "original_input": query["original_input"],
            "original_target": query["original_target"],
        }

    fewshot_queries = queries.map(
        create_fewshot_query,
        with_indices=True,
        num_proc=num_proc,
        desc="Creating few-shot queries",
    )

    return fewshot_queries


class Task(TaskInterface):
    def __init__(
        self,
        config: TaskConfig,
        root_task_id: str,
        subtask_id: Optional[str] = None,
    ):
        super().__init__()

        self.config = config
        self.root_task_id = root_task_id
        self.subtask_id = subtask_id

        self.dataset_format_num_proc = 4
        self.dataset_format_batched = False

    @property
    def task_id(self) -> str:
        if self.subtask_id is None:
            return self.root_task_id
        else:
            return f"{self.root_task_id}:{self.subtask_id}"

    def get_prepared_datasets(
        self,
        preparation_strategy: PreparationStrategy,
        shot_list: Optional[List[int]] = None,
        random_seed: int = 42,
    ) -> Union[Mapping[DatasetSplit, Dataset], Mapping[int, Dataset]]:
        datasets = self.get_datasets_raw()

        if preparation_strategy == PreparationStrategy.FINETUNING:
            # We don't need to do anything for finetuning
            return datasets

        if preparation_strategy == PreparationStrategy.PROMPT_BASED_TESTING:
            if shot_list is None:
                raise ValueError("shot_list must be specified for prompt-based testing")

            output = {}
            for num_shots in shot_list:
                output[num_shots] = make_nshot_dataset(
                    formatted_dataset=datasets,
                    prompt_builder_config=self.config.preparation_strategies.prompt_base_testing.prompt_builder,
                    shot_formatter=self._format_example_for_in_context_learning,
                    num_shots=num_shots,
                    random_seed=random_seed,
                    num_proc=self.dataset_format_num_proc,
                )

            return output

    def get_datasets_raw(self) -> Mapping[DatasetSplit, Dataset]:
        data_source = self._load_data_source()

        if self.config.split_file is not None:
            splitting_info = load_jsonnet(self.config.split_file)
            data_source = resplit_data_source(data_source, splitting_info)

        output = {}
        for split in sorted(data_source.keys()):
            dataset = data_source[split]
            output[split] = dataset.map(
                self.format_example,
                num_proc=self.dataset_format_num_proc,
                batched=self.dataset_format_batched,
                desc=f"Formatting `{split}` examples",
            )

        # Assign id to each example
        for split in sorted(output.keys()):
            output[split] = output[split].map(
                lambda example, idx: {"_genbench_idx": idx},
                with_indices=True,
                num_proc=self.dataset_format_num_proc,
                batched=False,
                desc=f"Assigning id to `{split}` examples",
            )

        return output

    def format_example(self, example: Mapping[str, Any]) -> Mapping[str, Any]:
        assert self.config.field_mapping is not None
        assert "input" in self.config.field_mapping
        assert "target" in self.config.field_mapping

        output = {
            "input": example[self.config.field_mapping["input"]],
            "target": example[self.config.field_mapping["target"]],
        }

        if "target_options" in self.config.field_mapping:
            output["target_options"] = example[
                self.config.field_mapping["target_options"]
            ]

        return output

    def evaluate_predictions(
        self,
        *,
        predictions: List[Mapping[str, Any]] = None,
        gold: Dataset = None,
    ) -> Mapping[str, float]:
        result = {}
        for metric_config in self.config.evaluation_metrics:
            hf_id = metric_config.hf_id
            if isinstance(hf_id, str):
                hf_id = [hf_id]

            metric = evaluate.load(*hf_id, revision=metric_config.git_commit_sha)

            preds_lst = [pred["target"] for pred in predictions]
            gold_lst = [g["target"] for g in gold]
            extra_kwargs = metric_config.compute_extra_kwargs or {}
            output: dict = metric.compute(
                predictions=preds_lst, references=gold_lst, **extra_kwargs
            )

            if output is None:
                raise ValueError(
                    f"Metric {metric_config.hf_id} returned None. "
                    f"Please check the metric implementation."
                )

            # Update output keys to include the metric id
            metric_id = "_".join(hf_id)
            output = {f"hf_{metric_id}__{k}": v for k, v in output.items()}

            result.update(output)

        return result

    def _load_data_source(
        self,
    ) -> Union[DatasetDict, Dataset, IterableDatasetDict, IterableDataset]:
        """
        Private method to load the data source based on the type specified in the configuration.

        The data source can be of two types: 'manual' or 'hf'.
        For 'manual' type, it loads JSON datasets from the specified test, validation, and train files.
        For 'hf' type, it loads datasets from the HuggingFace datasets hub using the given HuggingFace dataset ID(s)
        and the git commit SHA for the specified version of the dataset.

        Returns:
            Loaded dataset which can be any of the following types:
            DatasetDict, Dataset, IterableDatasetDict, IterableDataset.

        Raises:
            ValueError: If the specified data source type is not supported.
        """
        if self.config.data_source.type == "manual":
            data_files = {
                "test": self.config.data_source.test,
            }
            if self.config.data_source.validation is not None:
                data_files["validation"] = self.config.data_source.validation
            if self.config.data_source.train is not None:
                data_files["train"] = self.config.data_source.train

            return load_dataset("json", data_files=data_files)
        elif self.config.data_source.type == "hf":
            hf_id = self.config.data_source.hf_id
            if isinstance(hf_id, str):
                hf_id = [hf_id]

            return load_dataset(*hf_id, revision=self.config.data_source.git_commit_sha)
        else:
            raise ValueError(
                f"Unsupported data source type: {self.config.data_source.type}"
            )

    def _format_example_for_in_context_learning(
        self, example: Mapping[str, Any], random_seed: int
    ) -> Mapping[str, Any]:
        rng = np.random.RandomState(seed=random_seed + example["_genbench_idx"])
        prompt_config = (
            self.config.preparation_strategies.prompt_base_testing.prompt_builder
        )

        formatted_input = prompt_config.input_prefix + example["input"]

        if self.config.task_type == TaskType.MULTIPLE_CHOICE:
            choices = example["target_options"]
            if prompt_config.append_choices_to_input:
                input_choices = choices[:]
                if prompt_config.permute_choices:
                    input_choices = rng.permutation(sorted(input_choices))
                formatted_input += prompt_config.choices_prefix + "".join(
                    [
                        f"{prompt_config.choice_item_prefix}{c}{prompt_config.choice_item_postfix}"
                        for c in input_choices
                    ]
                )

            target = choices[example["target"]]
        elif self.config.task_type == TaskType.FREE_FORM:
            target = example["target"]
        elif self.config.task_type == TaskType.SEQUENCE_LABELING:
            target = prompt_config.sequence_labeling_separator.join(example["target"])
        else:
            raise ValueError(f"Unsupported task type: {self.config.task_type}")

        formatted_target = prompt_config.output_prefix + target

        return {
            "formatted_input": formatted_input,
            "formatted_target": formatted_target,
        }
