from typing import Any, Dict, List

import datasets
import numpy as np

# import evaluate
from genbench import Task


class DbcaDeprelTask(Task):
    """This task evaluates how well an NMT model generalises to a shifted distribution of
    dependency relations. In practice, this means that the test set includes novel
    (<head lemma>, <deprel>, <dependant lemma>) tuples (=compounds) that were not seen in
    the training set, while having similar relative frequencies of the lemmas and dependency
    relation tags (= elements of the compound tuples = atoms).
    """

    def evaluate_predictions(
        self,
        *,
        predictions: List[Dict[str, Any]] = None,
        gold: datasets.Dataset = None,
    ) -> Dict[str, float]:
        """Evaluate the predictions of the model against the gold data.
        For this task, the evaluation metric returns the BLEU and/or chrF score and the atom and
        compound divergences.
        Args:
            predictions: A list of dictionaries, where each dictionary contains the predicted
                         values for an example. The keys are strings and the values the model predictions.
            gold: A HuggingFace `datasets.Dataset` object containing the ground truth data for the task.
        Returns:
            A dictionary containing key-value pairs for the evaluation metric(s) computed on the predicted
            values. The keys are strings representing the name of the evaluation metric and the values are
            floating-point numbers.
        """

        # TODO: implement BLEU and chrF
        # preds_list = [pred["target"] for pred in predictions]
        # refs_list = [g["target"] for g in gold]

        # bleu = evaluate.load("bleu")
        # bleu_result = bleu.compute(predictions=preds_list, references=refs_list)
        # return {"BLEU": bleu_result['bleu']}
        return {"BLEU": 0.0}

    def chernoff_coef(self, vec1, vec2, alpha):
        """
        The Chernoff coefficient c is a similarity measure C_{alpha}(P||Q)
        = sum_k[p_k^alpha * q_k^(1-alpha)] e[0,1] between two (probability)
        distributions P and Q. The alpha parameter determines if we want to
        measure whether Q includes elements that are not in P.
        """
        if alpha < 0 or alpha > 1:
            raise ValueError("alpha must be in [0,1]")
        # use log to avoid underflow
        return np.sum(np.exp((np.log(vec1) * alpha) + (np.log(vec2) * (1 - alpha))), axis=1)

    def normalize_vector(self, vector):
        """Normalize a vector to have sum 1."""
        return np.nan_to_num(np.divide(vector, np.sum(vector)))

    def divergence(self, vec1, vec2, alpha):
        """
        Calculate divergence between two vectors.
        Atom divergence is 1 - Chernoff coefficient, with alpha=0.5.
        Compound divergence is 1 - Chernoff coefficient, with alpha=0.1.
        """
        return float(1 - self.chernoff_coef(self.normalize_vector(vec1), self.normalize_vector(vec2), alpha))

    def count_freqs(
        self,
        dataset,
    ):
        """TODO: Return the frequencies of atoms and compounds in the dataset."""
        pass
