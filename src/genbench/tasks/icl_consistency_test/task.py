from typing import Any, Dict, List
from genbench import Task

from sklearn.metrics import cohen_kappa_score
from pandas import DataFrame

import datasets

label_map_to_numeric = {'Impossible': 2,
                        'Inconclusive': 1,
                        'Correct': 0,
                        'True': 0,
                        'Always': 0,
                        'Yes': 0,
                        'Possible': 1,
                        'Never': 2,
                        'Incorrect': 2,
                        'False': 2,
                        'Sometimes': 1,
                        'No': 2,
                        'Maybe': 1,
                        'Guaranteed': 0,
                        'Neither': 1,
                        'no': 2,
                        'yes': 0,
                        'Not Duplicates': 2,
                        'Duplicates': 0,
                        'not duplicates': 2,
                        'duplicates': 0,
                        }

factors = ['balanced_labels', 'cross_task', 'diverse_context', 'n_shots', 'template', 'calibrate', ]


# @Task.register(IclConsistencyTestTask)
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
        # TODO:
        #  1. Insert some assert statements, assuming that we have the same data_IDs for all setups.
        #  2. For consistency metric (Cohen's kappa): mask out out-of-label-space predictions (-1)
        #  3. For consistency metric (Cohen's kappa): make sure that prediction vectors are aligned
        #  (according to data_IDs) [Order results_df similar to what I did in the analysis notebook.]

        gold_labels_numeric = {}
        gold_pandas = gold.to_pandas()
        for data_id in set(gold_pandas['data_ID']):
            gold_labels_numeric[str(data_id)] = gold_pandas.loc[
                gold_pandas['data_ID'] == data_id]['target_numeric'].to_list()[0]

        results_df = self._create_df(predictions, gold_labels_numeric)

        em = {factor: [] for factor in factors}
        em.update({
            'accuracy': [],
        })

        # Compute the exact match accuracy for each setup.
        for setup_ID in predictions:
            used_data = results_df.loc[results_df['setup_ID'] == setup_ID]
            temp = self._convert_numeric_id_to_dict(setup_ID, n_repititions=1)
            for factor in factors:
                em[factor] += temp[factor]

            em['accuracy'] += [(used_data['predictions_numeric'] == used_data['target_numeric']).mean()]

        # Compute the Cohen's kappa for consistency.
        try:
            kappas = {}
            for factor in factors:
                factor_present = results_df.loc[results_df[factor] == '1']['predictions_numeric']
                factor_absent = results_df.loc[results_df[factor] == '0']['predictions_numeric']
                kappas[factor] = cohen_kappa_score(factor_present, factor_absent)
        except:
            breakpoint()

        # Return the evaluation metrics.
        return {"exact_match_accuracy": em,
                "kappas": kappas}

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
        results_dict = {factor: [] for factor in factors}
        results_dict.update({
            'predictions_numeric': [],
            'target_numeric': [],
            'setup_ID': [],
        })

        for setup_ID in predictions:
            n_datapoints = len(predictions[setup_ID])
            results_dict['predictions_numeric'] += [self._label_to_numeric(predictions[setup_ID][data_ID]) for
                                                    data_ID in predictions[setup_ID].keys()]
            results_dict['target_numeric'] += [gold_labels[data_ID] for data_ID in predictions[setup_ID].keys()]
            results_dict['setup_ID'] += [setup_ID] * n_datapoints
            temp = self._convert_numeric_id_to_dict(setup_ID, n_repititions=n_datapoints)
            for factor in factors:
                results_dict[factor] += temp[factor]

        return DataFrame(results_dict)

    @staticmethod
    def _convert_numeric_id_to_dict(setup_id: str, n_repititions: int = 1) -> Dict[str, Any]:
        """Convert a numeric setup_ID to a interpretable dict.

        Args:
            id: A numeric ID.

        Returns:
            A dict containing factors as keys and the factor realisation as value.
        """
        setup_dict = {}
        for factor, value in zip(factors, setup_id):
            setup_dict[factor] = [value] * n_repititions

        return setup_dict

    @staticmethod
    def _label_to_numeric(label: str) -> int:
        """Convert a label to a numeric value.

        Args:
            label: A label.

        Returns:
            A numeric label.
        """
        if label in label_map_to_numeric:
            return label_map_to_numeric[label]
        else:
            return -1
