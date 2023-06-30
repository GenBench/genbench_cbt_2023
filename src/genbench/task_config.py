import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple, Union

import _jsonnet
import dataclass_factory

from genbench.api import TaskType
from genbench.utils.validation import is_valid_url


@dataclass
class DataSourceConfig:
    """
    Configuration class for specifying the data source.

    Parameters:
        type (`Literal["hf", "manual"]`):
            We allow submissions involving HuggingFace datasets or publicly accessible URIs to
            dataset files hosted with a date stamp (only one option is allowed).
            Option 1 ("hf"): Use a HuggingFace dataset, Option 2 ("manual"): Use a publicly accessible URI
        hf_id (`Optional[Union[str, Tuple[str, ...]]]`, optional):
            HuggingFace dataset id. e.g. 'snli', or ('super_glue', 'MultiRC') in case of datasets that
            are part of benchmarks. Only needed if `type` == "hf".
        git_commit_sha (`Optional[str]`, optional):
            Git commit sha of the data source.
            To ensure the HF dataset is read from the same version
            every time, you need to specify the commit SHA of HF dataset.
            You can find them in https://huggingface.co/datasets/<dataset-name>/commits/main
            Only needed if `type` == "hf".
        test (`Optional[str]`, optional):
            Test set URL. Only needed if `type` == "manual".
        train (`Optional[str]`, optional):
            Train set URL. Only needed if `type` == "manual".
        validation (`Optional[str]`, optional):
            Validation set URL. Only needed if `type` == "manual".

    Raises:
        AssertionError: If the data source type is "hf" and either `hf_id` or `git_commit_sha` is None.
        AssertionError: If the data source type is "manual" and any of the URLs provided is invalid.
    """

    type: Literal["hf", "manual"] = field(metadata={"help": "Type of the data source. e.g. 'hf'"})
    hf_id: Optional[Union[str, Tuple[str, str]]] = field(
        default=None, metadata={"help": "HuggingFace dataset id. e.g. 'glue'"}
    )
    git_commit_sha: Optional[str] = field(
        default=None,
        metadata={"help": "Git commit sha of the data source. e.g. '070042b....'"},
    )
    test: Optional[str] = field(
        default=None,
        metadata={"help": "Test set URL. e.g. 'https://example.com/test.jsonl'"},
    )
    train: Optional[str] = field(
        default=None,
        metadata={"help": "Train set URL. e.g. 'https://example.com/train.jsonl'"},
    )
    validation: Optional[str] = field(
        default=None,
        metadata={"help": "Validation set URL. e.g. 'https://example.com/val.jsonl'"},
    )

    def __post_init__(self):
        if self.type == "hf":
            assert self.hf_id is not None
            assert self.git_commit_sha is not None
            assert isinstance(self.hf_id, str) or (isinstance(self.hf_id, tuple) and len(self.hf_id) == 2)
        elif self.type == "manual":
            assert self.test is not None
            assert all([(url is None) or (is_valid_url(url)) for url in [self.test, self.train, self.validation]])
        else:
            raise ValueError(f"Invalid value for data source type: {self.type}. Must be one of ['hf', 'manual']")


@dataclass
class EvaluationMetricConfig:
    hf_id: Union[str, Tuple[str, str]] = field(metadata={"help": "HuggingFace metric id. e.g. 'accuracy'"})
    git_commit_sha: str = field(metadata={"help": "Git commit sha of the metric. e.g. '070042b....'"})
    best_score: float = field(metadata={"help": "Best value of the metric. e.g. 1.0"})
    compute_extra_kwargs: Optional[Dict[str, str]] = field(
        default=None,
        metadata={"help": "Extra kwargs to pass to the metric's compute method."},
    )

    def __post_init__(self):
        assert self.hf_id is not None
        assert self.git_commit_sha is not None
        assert isinstance(self.hf_id, str) or (isinstance(self.hf_id, tuple) and len(self.hf_id) == 2)

        assert self.best_score is not None, "Best value must be specified."


@dataclass
class FinetuningStrategyConfig:
    objective: Literal["maximum_likelihood"] = field(metadata={"help": "Objective of the finetuning strategy."})


@dataclass
class PromptBuilderConfig:
    """
    Configuration class for prompt generation.
    Currently, we follow BIG-bench options for prompt construction:
    https://github.com/google/BIG-bench/blob/main/docs/doc.md#optional-fields

    Parameters:
        instruction (str, optional):
            Instruction of the task. Will be prepended to the model's input. e.g. 'Add two numbers:'
        input_prefix (str, optional):
            Prefix of the model's input. Defaults to 'Q: '.
        output_prefix (str, optional):
            Prefix of the model's output. Defaults to 'A: '.
        choice_prefix (str, optional):
            Prefix of the model's choice. Defaults to '\n  choice: '.
        append_choices_to_input (bool, optional):
            Whether to append the choices to the model's input. Defaults to True.
        few_shot_example_separator (str, optional):
            Separator between the few-shot examples. Defaults to '\n'.
        stop_string (str, optional):
            Stop string to indicate the end of the input. Defaults to '\n\n'.

    """

    instruction_zero_shot: str = field(
        default="",
        metadata={
            "help": ("Instruction of the task. Will be prepended to the" " model's input. e.g. 'Add two numbers:'")
        },
    )
    instruction_few_shot: str = field(
        default="",
        metadata={
            "help": (
                "Instruction of the task. Will be prepended to the"
                " model's input. e.g. 'Add two numbers. Here are some examples:'"
            )
        },
    )
    input_prefix: str = field(default="Q: ", metadata={"help": "Prefix of the model's input."})
    output_prefix: str = field(default="\nA: ", metadata={"help": "Prefix of the model's output."})
    append_choices_to_input: bool = field(
        default=True,
        metadata={"help": "Whether to append the choices to the model's input."},
    )
    choices_prefix: str = field(
        default="\nchoices: \n",
        metadata={"help": "Prefix of the model's choice."},
    )
    choice_item_postfix: str = field(
        default="\n",
        metadata={"help": "Separator between the choices."},
    )
    choice_item_prefix: str = field(
        default="- ",
        metadata={"help": "Prefix of the model's choice item."},
    )
    sequence_labeling_separator: str = field(
        default=",",
        metadata={"help": "Separator between the sequence labeling tokens."},
    )
    permute_choices: bool = field(
        default=False,
        metadata={"help": "Whether to permute the choices."},
    )
    few_shot_example_separator: str = field(
        default="\n\n",
        metadata={"help": "Separator between the few-shot examples."},
    )
    stop_string: str = field(
        default="\n\n",
        metadata={"help": "Stop string to indicate the end of the input."},
    )


@dataclass
class PromptBaseTestingConfig:
    prompt_builder: PromptBuilderConfig = field(metadata={"help": "Prompt builder configuration."})


@dataclass
class PreparationStrategiesConfig:
    finetuning: Optional[FinetuningStrategyConfig] = field(
        default=None, metadata={"help": "Finetuning strategy configuration."}
    )
    prompt_based_testing: Optional[PromptBaseTestingConfig] = field(
        default=None, metadata={"help": "Prompt base testing configuration."}
    )


@dataclass
class TaskConfig:
    """
    Configuration class for defining a task.

    Parameters:
        name (str):
            Name of the task. e.g. 'Addition'
        description (str):
            Description of the task. e.g. 'Addition of two numbers'
        keywords (List[str]):
            Keywords of the task
        authors (List[str]):
            Authors of the task
        data_source (DataSourceConfig):
            Data source configuration
        has_validation_set (bool, optional):
            Whether the task provides a validation set. Defaults to False.
        has_train_set (bool, optional):
            Whether the task provides a train set. Defaults to False.
        task_type (Literal["free_form", "multi_choice", "sequence_labeling"]):
            Type of the task. e.g. 'free_form'
        field_mapping (Optional[Dict[str, str]], optional):
            Mapping from the fields in the data source to the fields that the task ('input', 'target') expects.
            Defaults to None.
        free_form_output_regex (Optional[str], optional):
            Regex to extract the output from the free form answer. Defaults to None.
        split_file (Optional[str], optional):
            Path to the split file. Defaults to None.
        evaluation_metric (Optional[List[EvaluationMetricConfig]], optional):
            Evaluation metric configuration. Defaults to None.
        preparation_strategies (PreparationStrategiesConfig):
            Preparation strategies configuration.
    """

    name: str = field(metadata={"help": "Name of the task. e.g. 'Addition'"})
    description: str = field(metadata={"help": "Description of the task. e.g. 'Addition of two numbers'"})
    keywords: List[str] = field(
        metadata={"help": "Keywords of the task"},
    )
    authors: List[str] = field(
        metadata={"help": "Authors of the task"},
    )

    data_source: DataSourceConfig = field(
        metadata={"help": "Data source configuration"},
    )

    task_type: TaskType = field(
        metadata={"help": "Type of the task. e.g. 'free_form'"},
    )

    preparation_strategies: PreparationStrategiesConfig = field(
        metadata={"help": "Preparation strategies configuration."}
    )

    field_mapping: Optional[Dict[str, str]] = field(
        default=None,
        metadata={
            "help": (
                "Mapping from the fields in the data source " "to the fields that the task ('input','target') expects."
            )
        },
    )

    evaluation_metrics: Optional[List[EvaluationMetricConfig]] = field(
        default=None,
        metadata={"help": "Evaluation metric configuration"},
    )

    split_file: Optional[str] = field(
        default=None,
        metadata={"help": "split filename"},
    )

    free_form_output_regex: Optional[str] = field(
        default=None,
        metadata={"help": "Regex to extract the output from the free form answer"},
    )

    has_validation_set: bool = field(
        default=False,
        metadata={"help": "Whether the task provides a validation set"},
    )
    has_train_set: bool = field(
        default=False,
        metadata={"help": "Whether the task provides a train set"},
    )

    def __post_init__(self):
        if self.task_type == "free_form" and self.free_form_output_regex is None:
            raise ValueError("Task type is free_form but no free_form_output_regex is provided.")

        if self.field_mapping is not None:
            assert "input" in self.field_mapping, "Field mapping must contain 'input' field."
            assert "target" in self.field_mapping, "Field mapping must contain 'target' field."

        assert self.keywords is not None and len(self.keywords) > 0, "Keywords must be provided for the task."

        assert self.authors is not None and len(self.authors) > 0, "Authors must be provided for the task."

        assert self.preparation_strategies is not None, "Preparation strategies must be provided for the task."

    @staticmethod
    def from_jsonnet(jsonnet_str: Optional[str] = None, jsonnet_path: Optional[Path] = None) -> "TaskConfig":
        if jsonnet_str is None and jsonnet_path is None:
            raise ValueError("Either jsonnet_str or jsonnet_path must be provided.")
        elif jsonnet_str is not None and jsonnet_path is not None:
            raise ValueError("Only one of jsonnet_str or jsonnet_path must be provided.")

        if jsonnet_str is None:
            jsonnet_str = jsonnet_path.read_text()

        json_str = _jsonnet.evaluate_snippet("snippet", jsonnet_str)
        json_dict = json.loads(json_str)

        factory = dataclass_factory.Factory()
        config: TaskConfig = factory.load(json_dict, TaskConfig)
        return config

    def to_json(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), indent=4))
