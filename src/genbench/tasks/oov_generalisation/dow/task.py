from genbench import Task


class OovGeneralisationDow(Task):
    
    def get_datasets_raw(self) -> Mapping[str, datasets.Dataset]:
        """Get the raw dataset.

        By default, this method loads the dataset specified in the task's
        config.jsonnet, and re-split it based on split.json if it exists.
        If the task creator wishes to mix and match data points, they can
        override this method.

        Returns:
            A dictionary containing key-value pairs for the raw datasets.
            The keys are strings representing the name of the dataset split
            (e.g., "train", "validation", "test") and the values are
            HuggingFace `datasets.Dataset` objects containing the raw data for the corresponding split.
        """
        ...