from typing import Any, Dict, List

import datasets
from scipy.stats import pearsonr
from sklearn.metrics import accuracy_score

from genbench import Task
from genbench.utils.logging import get_logger


logger = get_logger(__name__)


class FrequencyBasedMathematicsTask(Task):
    """Python implementation of the FrequencyBasedMathematics task.

    This LLM task assess to what extent the computation of mathematical expressions
    depends on the frequency of the individual terms during pretraining.
    The test is inspired by the work of Razeghi et al (2022).
    It defines a generalisation score as 1 - abs(pearsonsR(term_freq, score))

    To facilitate this, it reimplements the following default functions:
    - TODO list functions to be reimplemented
    - __init__ : this function checks if a file with term frequences is
                 added by the user, and warns the user if it is not
    - evaluate_predictions: this function implements the generalisation
                metric used for this task
    """

    def evaluate_predictions(
        self,
        *,
        predictions: List[Dict[str, Any]] = None,
        gold: datasets.Dataset = None,
        term_freqs: Dict[str, int] = None,
    ) -> Dict[str, float]:
        """Evaluate the predictions of the model against the gold data.

        For this task, the evaluation metric returns the minimum accuracy
        among different prompts (i.e. if one of the prompts returns a wrong
        answer, the score is 0 for that example).

        Args:
            predictions: A list of dictionaries, where each dictionary contains the predicted
                         values for an example. The keys are strings and the values the model predictions.
            gold: A HuggingFace `datasets.Dataset` object containing the ground truth data for the task.
            term_freqs: A dictionary that maps the terms 10-30 to their frequencies in the pretraining corpus

        Returns:
            A dictionary containing key-value pairs for the evaluation metric(s) computed on the predicted
            values. The keys are strings representing the name of the evaluation metric and the values are
            floating-point numbers.
        """

        if term_freqs is None:
            raise Exception(
                "This evaluation requires information about term frequencies in the pretraining corpus. \
                They should be provided by the user. \
                For more information, we refer to the readme of this task."
            )

        scores, freqs = [], []

        preds_list = [pred["target"] for pred in predictions]
        refs_list = [g["target"] for g in gold]

        for n in range(40):
            # Fetch all accuracy scores for the predictions
            for prediction in predictions:
                acc = accuracy_score(preds_list[n : n + 20], refs_list[n : n + 20])
                freq = term_freqs[n + 10]
                scores.append(acc)
                freqs.append(freq)

        corr = pearsonr(scores, freqs)[0]

        return {"gen_score": 1 - abs(corr), "accuracy": sum(scores) / len(scores)}
