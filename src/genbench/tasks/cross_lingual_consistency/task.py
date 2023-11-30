from collections import defaultdict
from typing import Any, Dict, List, Mapping, Optional

import datasets
import numpy as np
from datasets import load_dataset

from genbench import Task
from genbench.api import PreparationStrategy

class CrossLingualConsistencyTask(Task):
    def _load_data_source(
        self,
        mini,
        lang1,
        lang2,
    ):
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
            if mini:
                file_path = self.config.data_source.test + "BMLAMA17/"
            else:
                file_path = self.config.data_source.test + "BMLAMA53/"

            data_files = dict()
            for lang in [lang1, lang2]:
                data_files[lang] = file_path + lang + ".tsv"
            """
            data_files = {
                "test": self.config.data_source.test,
            }
            """
            if self.config.data_source.validation is not None:
                data_files["validation"] = self.config.data_source.validation
            if self.config.data_source.train is not None:
                data_files["train"] = self.config.data_source.train

            return load_dataset("csv", data_files=data_files, delimiter="\t")
            # return load_dataset("json", data_files=data_files, field=None)
        elif self.config.data_source.type == "hf":
            hf_id = self.config.data_source.hf_id
            if isinstance(hf_id, str):
                hf_id = [hf_id]

            return load_dataset(*hf_id, revision=self.config.data_source.git_commit_sha)
        else:
            raise ValueError(f"Unsupported data source type: {self.config.data_source.type}")

    def get_datasets_raw(self, mini=True, lang1="en", lang2="es"):
        data_source = self._load_data_source(mini=mini, lang1=lang1, lang2=lang2)

        """
        if self.config.split_file is not None:
            split_file_path = get_task_dir(self.root_task_id, self.subtask_id) / self.config.split_file
            splitting_info = load_jsonnet(split_file_path)
            data_source = resplit_data_source(data_source, splitting_info)
        """

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

    def get_prepared_datasets(
        self,
        preparation_strategy: PreparationStrategy,
        shot_list: Optional[List[int]] = None,
        random_seed: int = 42,
        mini=True,
        lang1=None,
        lang2=None,
    ):
        if not mini:
            raise ValueError("Value for 'mini=True/False' is required for this task")
        if not lang1 or not lang2:
            raise ValueError("Values for 'lang1=' and 'lang2=' are required for this task")

        if preparation_strategy == PreparationStrategy.FINETUNING:
            if self.config.preparation_strategies.finetuning is None:
                raise ValueError("Finetuning preparation strategy is not supported for this task")

        datasets = self.get_datasets_raw(mini=mini, lang1=lang1, lang2=lang2)

        # datasets is a dict of language_id -> Dataset
        lang1_ds = datasets[lang1]
        lang2_ds = datasets[lang2]

        # They all have the same length (i.e. they are translation of each other)
        assert len(lang1_ds) == len(lang2_ds)

        # Each of them contains instances of the form:
        # {
        #   "input": "The capital of Canada ",
        #   "target": "Ottawa",
        #   "target_options": [
        #       "Beijing",
        #       "Tokyo",
        #       "Ottawa",
        #   ],
        #   "_genbnech_idx": <some index>
        # }

        # Add language identifier to each instance
        lang1_ds = lang1_ds.map(lambda x: {"lang": lang1})
        lang2_ds = lang2_ds.map(lambda x: {"lang": lang2})

        # Concatenate the datasets
        from datasets import concatenate_datasets

        final_dataset = concatenate_datasets([lang1_ds, lang2_ds])

        return final_dataset

    def evaluate_predictions(
        self,
        *,
        predictions: List[Mapping[str, Any]] = None,
        gold: datasets.Dataset = None,
    ) -> Dict[str, float]:
        def softmax(x):
            """Compute softmax values for each sets of scores in x."""
            return np.exp(x) / np.sum(np.exp(x), axis=0)

        # Make sure that the predictions are in the same order as the gold dataset
        assert len(predictions) == len(gold)

        # Just to make sure the gold dataset is the same as the one we generated in `get_prepared_datasets`
        assert "lang" in gold.features
        assert "_genbnech_idx" in gold.features

        # Also, make sure that predictions contain logprobs for each option
        assert all(
            "target_option_logprobs" in pred and len(pred["target_option_logprobs"]) == len(pred["target_options"])
            for pred in predictions
        )

        # Group the prediction and instances such that we have:
        # _genbnech_idx -> {
        #    "lang_id_1": { ...data_instance..., target_option_logprobs: ... }
        #    "lang_id_2": { ...data_instance..., target_option_logprobs: ... }
        # },

        grouped_examples = defaultdict(dict)
        for pred, gold in zip(predictions, gold):
            original_idx = gold["_genbnech_idx"]
            lang = gold["lang"]
            grouped_examples[original_idx][lang] = {
                **gold,
                **pred,
            }

        CLC_score = 0
        count = 0
        langs = []
        # Now, we compute the cross lingual consistency score
        for idx, example in grouped_examples.items():
            # Rerank the options based on the logprobs
            for lang, data in example.items():
                if len(langs) < 2:
                    langs.append(lang)

                logprobs = data["target_option_logprobs"]
                sorted_options = sorted(
                    zip(data["target_options"], logprobs),
                    key=lambda x: x[1],
                    reverse=False,
                )
                sorted_options, logprobs = zip(*sorted_options)
                grouped_examples[idx][lang]["target_options"] = list(sorted_options)
                grouped_examples[idx][lang]["target_option_logprobs"] = list(logprobs)

            # Compute the cross lingual consistency score
            ranking1 = grouped_examples[idx][langs[0]]["target_options"]
            ranking2 = grouped_examples[idx][langs[1]]["target_options"]

            order = [len(ranking1) - i for i in range(len(ranking1))]
            order = np.array(order)
            weight = softmax(order)

            for j in range(len(ranking1)):
                set1 = {ranking1.index(i) for i in ranking1[: j + 1]}
                set2 = {ranking2.index(i) for i in ranking2[: j + 1]}

                cover = set1.intersection(set2)
                CLC_score += weight[j] * (len(cover) / len(set1))

            count += 1
        CLC_score /= count

        # Compute the final score
        result = {
            "cross_lingual_consistency": CLC_score,
        }

        return result

    def format_example(self, example: Mapping[str, Any]) -> Mapping[str, Any]:
        if self.config.field_mapping is None:
            assert "input" in example
            assert "target" in example
            output = {}
        else:
            assert "input" in self.config.field_mapping
            assert "target" in self.config.field_mapping

            output = {
                "input": example[self.config.field_mapping["input"]],
                "target": example[self.config.field_mapping["target"]],
            }

            if "target_options" in self.config.field_mapping:
                output["target_options"] = example[self.config.field_mapping["target_options"]]

        return output
