import random
from typing import Dict, List

import datasets
import numpy as np
from more_itertools import chunked

from genbench import Task


# @Task.register("nl_codesearch_mrr:codesearchnet_adv") this doesnt seem to work
class NlCodesearchMrrCodesearchnetAdv(Task):
    def get_dataset_raw(self, n_distractors) -> Dict[str, datasets.Dataset]:
        """Create the dataset adding n distractor pair (original comment, random code snippet) for ranking.

        Args:
            n_distractors: the number of randomly sampled distractor code for each ranking chunk

        Returns:
            A dictionary containing key-value pairs for the raw datasets.
            The keys are strings representing the name of the dataset split
            (e.g., "train", "validation", "test") and the values are
            HuggingFace `datasets.Dataset` objects containing the original pair and the distractors for the test split.
            The train split only contains the original dataset.
        """
        # Load the raw datasets
        raw_datasets: Dict[str, datasets.Dataset] = self._load_data_source()
        output: Dict[str, datasets.Dataset] = {}
        # Set random seed for consistency
        random.seed(42)
        # Create 49 distractors for each item
        for split, dataset in raw_datasets.items():
            if split == "test":
                new_dataset = datasets.Dataset.from_dict({})
                for item in dataset:
                    # Add comment-code pair to new dataset
                    new_dataset = new_dataset.add_item(item)
                    other_items = [other_item for other_item in dataset if other_item != item]
                    # Randomly select 49 other items
                    random_items = random.sample(other_items, n_distractors)
                    # Split input into comment and code
                    input_parts = item["input"].split("[SEP]")
                    for random_item in random_items:
                        # Split random input into comment and code
                        random_input_parts = random_item["input"].split("[SEP]")
                        # Combine the "input" fields of the original and random items
                        new_input = input_parts[0] + "[SEP]" + random_input_parts[1]
                        new_item = {"input": new_input, "target": 0, "target_options": item["target_options"]}
                        # Add distractor comment-code pair to new dataset
                        new_dataset = new_dataset.add_item(new_item)
                output[split] = new_dataset
            else:
                output[split] = dataset
        return output

    def evaluate_predictions(
        self, predictions: List[Dict[str, float]], gold: datasets.Dataset, n_distractors
    ) -> Dict[str, float]:
        """Calculate the MRR score in chunks. One chunk consist of a true comment-code pair and n number of distractors
        This function assumes that the predictions were made and passed onto this function unshuffled.
        The test data is ordered with each true pair followed by n number of distractors
         Args:
             predictions: A list of dictionaries, where each dictionary contains the predicted values for an example.
                          The keys are strings and the values are floats (logit scores or similarity values).
             gold: A HuggingFace `datasets.Dataset` object containing the ground truth data for the task.
             n_distractors:  Number of distractor comment-code pair for each true pair.
                             Must be the same number as in the get_dataset_raw function

         Returns:
             A dictionary containing key-value pairs for the evaluation metric(s) computed on the predicted
             values. The keys are strings representing the name of the evaluation metric and the values are
             floating-point numbers.
        """
        ranks = []

        batched_predictions = chunked(predictions, n_distractors + 1)

        for batch_idx, predictions in enumerate(batched_predictions):
            correct_score = predictions[0]["score"]
            scores = np.array([prediction["score"] for prediction in predictions])
            rank = np.sum(scores >= correct_score)
            ranks.append(rank)
        mean_mrr = np.mean(1.0 / np.array(ranks))

        return {"mean mrr": mean_mrr}
