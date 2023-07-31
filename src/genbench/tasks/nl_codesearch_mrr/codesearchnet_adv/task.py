from genbench import Task

@Task.register("nl_codesearch_mrrcodesearchnet_adv")
class NlCodesearchMrrCodesearchnetAdv(Task):

    def get_dataset_raw(self) -> Dict[str, datasets.Dataset]:
            """Create the dataset by mixing every three data instance together.

            Args:
                None

            Returns:
                A dictionary containing key-value pairs for the raw datasets.
                The keys are strings representing the name of the dataset split
                (e.g., "train", "validation", "test") and the values are
                HuggingFace `datasets.Dataset` objects containing the raw data for the corresponding split.
            """
            # Load the raw datasets
            print("kaki")
            raw_datasets: Dict[str, datasets.Dataset] = self._load_data_source()

            # Mix every three data instances together per each split
            output: Dict[str, datasets.Dataset] = {}
            for split, dataset in raw_datasets.items():
                # Combine every three data instances together
                dataset = dataset.map(self._magic_combo, batched=True, batch_size=3)

                # Maybe do additional processing/formatting here
                dataset = dataset.map(self.format_example)

                output[split] = dataset

            return output

    def _magic_combo(self, examples: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
        """Combine every three data instances together.

        Args:
            examples: A dictionary containing key-value pairs for the data instances.
                The keys are strings representing the name of the data instance
                (e.g., "input", "target") and the values are lists containing
                the data instance values.

        Returns:
            A dictionary containing key-value pairs for the combined data instances.
            The keys are strings representing the name of the data instance
            (e.g., "input", "target") and the values are lists containing
            the combined data instance values.
        """
        
        single_example: Dict[str, Any] = {}

        # Perform some cool mixing magic here
        # ...

        # HuggingFace datasets.Dataset.map() expects
        # a dictionary of lists as output
        output = {k: [v] for k, v in single_example.items()}

        return output
            
            
def main():
    task =  NlCodesearchMrrCodesearchnetAdv()
    task.get_dataset_raw()
    
if __name__ == '__main__':
    main()