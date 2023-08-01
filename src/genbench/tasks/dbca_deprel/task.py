from typing import Any, Dict, List
import datasets
from sacrebleu.metrics import BLEU
from genbench import Task

class DbcaDeprelTask(Task):
    """This task evaluates how well an NMT model generalises to a shifted distribution of
    dependency relations. In practice, this means that the test set includes novel
    (<head lemma>, <deprel>, <dependant lemma>) tuples (=compounds) that were not seen in
    the training set, while having the same distribution of the lemmas and dependency
    relation tags (= elements of the compound tuples = atoms).
    
    To facilitate this, it reimplements the following default functions:
    - evaluate_predictions: this function implements the generalisation
                metric used for this task
    """

    def evaluate_predictions(
        self,
        *,
        predictions: List[Dict[str, Any]] = None,
        gold: datasets.Dataset = None,
    ) -> Dict[str, float]:
        """Evaluate the predictions of the model against the gold data.
        For this task, the evaluation metric returns the BLEU or chrF score and the atom and
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
        preds_list = [pred["target"] for pred in predictions]
        refs_list = [g["target"] for g in gold]

        bleu = BLEU()
        bleu_result = bleu.corpus_score(preds_list, [refs_list])

        return {"BLEU": bleu_result}
