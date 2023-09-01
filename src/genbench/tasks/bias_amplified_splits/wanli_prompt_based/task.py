from typing import Any, Dict, Mapping

from datasets import Dataset

from genbench import Task
from genbench.api import DatasetSplit
from genbench.task import resplit_data_source
from genbench.utils.file import load_jsonnet
from genbench.utils.tasks import get_task_dir


LABEL2VERBALIZER = {"entailment": "yes", "neutral": "maybe", "contradiction": "no"}


class BiasAmplifiedSplitsWanliPromptBased(Task):
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
            "input": f"Sentence 1: {example['premise']}\nSentence 2: {example['hypothesis']}",
            "target": LABEL2VERBALIZER[example["gold"]],
        }

    def get_datasets_raw(self) -> Mapping[DatasetSplit, Dataset]:
        data_source = self._load_data_source()

        # There is an assertion that tests if all of the split names ('train', 'validation', 'test')
        # also exist in the dataset originally.
        # in WANLI there's only a test set that is used for validation.
        # To define a validation set without turning on the assertion, we must "fake" one.
        data_source["validation"] = data_source["test"]

        if self.config.split_file is not None:
            split_file_path = get_task_dir(self.root_task_id, self.subtask_id) / self.config.split_file
            splitting_info = load_jsonnet(split_file_path)
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
            assert all([f in output[split].column_names for f in ["input", "target"]])

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
