from genbench import Task
from typing import Any, Callable, List, Mapping, Optional, Union, Dict
from datasets import Dataset, DatasetDict, IterableDataset, IterableDatasetDict

WANLI_LABEL2INT = {'entailment': 0, 'neutral': 1, 'contradiction': 2}


class BiasAmplifiedSplitsWanli(Task):
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
            depending on the task type.Œ
        """
        return {
            "input": f"{example['premise']} </s> {example['hypothesis']}",
            "target": WANLI_LABEL2INT[example["gold"]],
        }

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
        data_source = super(BiasAmplifiedSplitsWanli)._load_data_source()
        data_source['validation'] = data_source['test']
        return data_source

