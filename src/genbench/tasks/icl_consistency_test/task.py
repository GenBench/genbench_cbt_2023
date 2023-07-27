from typing import Any, Dict, List, Tuple
from genbench import Task

from sklearn.metrics import cohen_kappa_score
from pandas import DataFrame

import datasets

LABELS = [['Correct', 'True', 'Always', 'Yes', 'Guaranteed', 'Duplicates'],  # `correct` labels
          ['Inconclusive', 'Possible', 'Sometimes', 'Maybe', 'Neither'],  # `neutral` labels
          ['Impossible', 'Never', 'Incorrect', 'False', 'No', 'Not Duplicates'], ]  # `incorrect` labels

LABEL_TO_NUMERIC = {}
LABEL_TO_NUMERIC.update(dict([(label, i) for i, label_subset in enumerate(LABELS) for label in label_subset]))
LABEL_TO_NUMERIC.update(dict([(label.lower(), i) for i, label_subset in enumerate(LABELS) for label in label_subset]))

factors = [
    'balanced_labels',
    'one_label',
    'cross_task',
    'cross_instructions',
    'n_shots',
    'instructions',
    'instruction_quality',
]


class IclConsistencyTestTask(Task):
    """Python implementation of the ICL consistency test task."""

    def evaluate_predictions(
            self,
            *,
            predictions: Dict[str, Dict[str, Any]],
            gold: datasets.Dataset,
    ) -> Dict[str, Any]:
        """Evaluate the predictions of the model against the gold data.
        Calculating exact match accuracy plus consistency across all setups (Cohen's kappa).

        Args:
            predictions: A dictionary of dictionary, where the keys of the outer dictionary contains
                         the setup_IDs and the inner dictionary the data_IDs. The values of the inner dictionary
                         are the predictions for the example. The keys are strings and the values can be any type.
            gold: A HuggingFace `datasets.Dataset` object containing the ground truth data for the task.

        Returns:
            A dictionary containing key-value pairs for the evaluation metric(s) computed on the predicted
            values. The keys are strings representing the name of the evaluation metric and the values are
            floating-point numbers.
        """
        self._set_factors()

        gold_pandas = gold.to_pandas()
        gold_pandas['data_ID'] = gold_pandas['data_ID'].astype(str)
        gold_labels_numeric = gold_pandas.set_index('data_ID')['target_numeric'].to_dict()

        results_df = self._create_df(predictions, gold_labels_numeric)
        results_df = results_df.sort_values(by=['setup_ID', 'data_ID'])
        self._assert_equal_data_ids(results_df)

        # Compute the exact match accuracy for each setup.
        em = {factor: [] for factor in self.factors + ['accuracy']}
        for setup_ID, setup_predictions in results_df.groupby('setup_ID'):
            temp = self._convert_numeric_id_to_dict(setup_ID, n_repetitions=1)
            for factor in self.factors:
                em[factor].extend(temp[factor])
            em['accuracy'].append(
                (setup_predictions['predictions_numeric'] == setup_predictions['target_numeric']).mean())

        # Compute the Cohen's kappa for consistency.
        kappas = {}
        for factor in self.factors:
            factor_present = results_df.loc[results_df[factor] == '1']['predictions_numeric']
            factor_absent = results_df.loc[results_df[factor] == '0']['predictions_numeric']

            # mask out predictions that are out-of-label-distribution 
            mask = [(f1 != -1 and f2 != -1) for f1, f2 in zip(factor_absent, factor_present)]
            try:
                factor_present, factor_absent = factor_present[mask], factor_absent[mask]
            except:
                breakpoint()

            kappas[factor] = cohen_kappa_score(factor_present, factor_absent)

        # Return the evaluation metrics.
        return {"exact_match_accuracy": em,
                "kappas": kappas}

    def add_factor(self, data: Tuple[Dict, Dict], factor: str) -> Dict[str, Dict[str, Any]]:
        """Concatenate the data with the factor present and absent and update the setup_IDs accordingly. Also add the
           respective factor to the list of factors.

        Args:
            data: A tuple containing predictions, where the first element are predictions with factor absent and the
                    second element are predictions with factor present.
            factor: A string giving the name of the added factor.

        """

        # Update the setup_IDs of the data by appending a 0 when the factor is absent or 1 when the factor is present.
        setup_ids0 = list(data[0].keys())
        setup_ids1 = list(data[1].keys())

        for setup_id0, setup_id1 in zip(setup_ids0, setup_ids1):
            updated_id0 = setup_id0 + '0'
            updated_id1 = setup_id1 + '1'
            data[0][updated_id0] = data[0].pop(setup_id0)
            data[1][updated_id1] = data[1].pop(setup_id1)

        # Add factor to list of factors.
        self._set_factors()
        self.factors.append(factor)

        return {**data[0], **data[1]}

    def remove_factor(self, data: datasets.Dataset, factor: str, keep_present: bool = False) -> datasets.Dataset:
        """Remove data of factor and update the setup_IDs accordingly. Also remove the
           respective factor from the list of factors. Keep_present determines whether to keep data with the factor
           present or absent.

        Args:
            data: The dataset as obtained by the get_prepared_datasets() method.
            factor: A string with the name of the factor to remove.
            keep_present: whether to keep data with the factor present or absent.
        """
        self._set_factors()
        #breakpoint()
        len_setup_ID_preamble = 4
        index_factor = self.factors.index(factor) + len_setup_ID_preamble
        realisation_to_keep = str(int(keep_present))

        # filter out all unwanted datapoints and adapt setup_IDs to exclude factor
        data = data.filter(lambda x: x['setup_ID'][index_factor] == realisation_to_keep)
        data = data.map(lambda x: {**x, "setup_ID": x["setup_ID"][:index_factor] + x["setup_ID"][index_factor + 1:]} )

        # Remove factor from list of factors.
        
        self.factors.pop(self.factors.index(factor))

        return data

    def _create_df(self, predictions: Dict[str, Dict[str, Any]], gold_labels: Dict[str, int]) -> DataFrame:
        """Create a dataframe containing all predictions, gold labels and labels.

        Args:
            predictions: A dictionary of dictionary, where the keys of the outer dictionary contains
                         the setup_IDs and the inner dictionary the data_IDs. The values of the inner dictionary
                         are the predictions for the example. The keys are strings and the values can be any type.
            gold: A dictionary, where the keys are the data_IDs and the values are the gold labels for the example.
                         The keys are strings and the values can be any type.

        Returns:
            A pandas dataframe containing the predictions and gold data.
        """
        additional_keys = ['predictions_numeric', 'target_numeric', 'setup_ID', 'data_ID']
        results_dict = {factor: [] for factor in self.factors + additional_keys}

        for setup_ID, predictions_setup in predictions.items():
            data_ids = list(predictions_setup.keys())
            n_datapoints = len(data_ids)

            results_dict['data_ID'].extend(data_ids)
            results_dict['setup_ID'].extend([setup_ID] * n_datapoints)
            results_dict['target_numeric'].extend(gold_labels[data_id] for data_id in data_ids)
            results_dict['predictions_numeric'].extend(self._label_to_numeric(predictions_setup[data_id]) for
                                                       data_id in data_ids)

            temp = self._convert_numeric_id_to_dict(setup_ID, n_repetitions=n_datapoints)
            for factor in self.factors:
                results_dict[factor].extend(temp[factor])

        return DataFrame(results_dict)

    def _set_factors(self):
        if not hasattr(self, 'factors'):
            self.factors = factors

    def _convert_numeric_id_to_dict(self, setup_id: str, n_repetitions: int = 1) -> Dict[str, Any]:
        """Convert a numeric setup_ID to a interpretable dict.

        Args:
            id: A numeric ID of the form `id_1010101' where each digit represents a factor.

        Returns:
            A dict containing factors as keys and the factor realisation as value.
        """
        setup_id = setup_id.split('_')[1]

        setup_dict = {}
        for factor, value in zip(self.factors, setup_id):
            setup_dict[factor] = [value] * n_repetitions

        return setup_dict

    @staticmethod
    def _label_to_numeric(label: str) -> int:
        """Convert a label to a numeric value.

        Args:
            label: A label.

        Returns:
            A numeric label.
        """
        return LABEL_TO_NUMERIC[label] if label in LABEL_TO_NUMERIC else -1

    @staticmethod
    def _assert_equal_data_ids(results_df: DataFrame) -> None:
        """Assert that all data_IDs are the same for all setups.

        Args:
            results_df: A pandas dataframe containing the predictions and gold data.
        """
        used_data_ids = results_df['data_ID'].unique()
        for setup_ID in results_df['setup_ID'].unique():
            assert used_data_ids.sort() == results_df.loc[results_df['setup_ID'] == setup_ID][
                'data_ID'].unique().sort(), \
                "Not all data_IDs are the same for all setups. Check for missing predictions!"
