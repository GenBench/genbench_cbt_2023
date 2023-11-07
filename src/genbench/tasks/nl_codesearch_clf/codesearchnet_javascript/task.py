import random
from typing import Dict

import datasets

from genbench import Task


class NlCodesearchClfCodesearchnetJavascript(Task):
    def get_dataset_raw(self) -> Dict[str, datasets.Dataset]:
        """Create the dataset adding a negative sample for each code comment/query

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
        for split, dataset in raw_datasets.items():
            if split == "test":
                new_dataset = datasets.Dataset.from_dict({})
                for item in dataset:
                    # Add comment-code pair to new dataset
                    new_dataset = new_dataset.add_item(item)
                    other_items = [other_item for other_item in dataset if other_item != item]
                    # Randomly select other item
                    random_item = random.sample(other_items, 1)
                    # Split input into comment and code
                    input_parts = item["input"].split("[CODESPLIT]")
                    # Split random input into comment and code
                    random_input_parts = random_item[0]["input"].split("[CODESPLIT]")
                    # Combine the "input" fields of the original and random items
                    new_input = input_parts[0] + "[CODESPLIT]" + random_input_parts[1]
                    new_item = {"input": new_input, "target": 0, "target_options": item["target_options"]}
                    # Add negative sample comment-code pair to new dataset
                    new_dataset = new_dataset.add_item(new_item)
                output[split] = new_dataset
            else:
                output[split] = dataset
        return output
