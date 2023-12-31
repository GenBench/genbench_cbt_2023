import random
from typing import Dict, List

import datasets
import numpy as np

from genbench import Task


def chunked(iterable, chunk_size):
    """
    Split an iterable into chunks of a specified size.

    Args:
        iterable: The iterable to be chunked.
        chunk_size: The size of each chunk.

    Returns:
        A generator that yields chunks of the iterable.
    """
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero")

    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk


class NlCodesearchMrrCodesearchnetRuby(Task):
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
                # Convert dataset to list for easier manipulation
                dataset_list = list(dataset)

                new_data = []

                for idx, item in enumerate(dataset_list):
                    new_data.append(item)

                    # Create other_items list once and then simply exclude the current item during sampling
                    other_items = dataset_list[:idx] + dataset_list[idx + 1 :]
                    random_items = random.sample(other_items, n_distractors)

                    input_parts = item["input"].split("[CODESPLIT]")

                    for random_item in random_items:
                        random_input_parts = random_item["input"].split("[CODESPLIT]")
                        new_input = input_parts[0] + "[CODESPLIT]" + random_input_parts[1]
                        new_item = {"input": new_input, "target": 0, "target_options": item["target_options"]}
                        new_data.append(new_item)

                # Convert list back to HuggingFace dataset
                output[split] = datasets.Dataset.from_dict({k: [dic[k] for dic in new_data] for k in new_data[0]})
            else:
                output[split] = dataset
        return output

    def evaluate_predictions(self, predictions: List[Dict[str, float]], n_distractors) -> Dict[str, float]:
        """Calculate the MRR score in chunks. One chunk consist of a true comment-code pair and n number of distractors
        This function assumes that the predictions were made and passed onto this function unshuffled.
        The test data is ordered with each true pair followed by n number of distractors
         Args:
             predictions: A list of dictionaries, where each dictionary contains the predicted values for an example.
                          The keys are strings and the values are floats (logit scores or similarity values).
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
