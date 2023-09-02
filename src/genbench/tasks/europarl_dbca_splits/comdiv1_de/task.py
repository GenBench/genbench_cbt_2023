from collections import OrderedDict
from typing import Any, List, Mapping

import evaluate
import numpy as np
from datasets import Dataset

from genbench import Task
from genbench.api import EvaluationResult, TaskType
from genbench.utils.logging import get_logger


logger = get_logger(__name__)


class EuroparlDbcaSplitsComdiv1De(Task):
    """This task evaluates how well an NMT model generalises to a shifted distribution of
    dependency relations. In practice, this means that the test set includes novel
    (<head lemma>, <deprel>, <dependant lemma>) tuples (=compounds) that were not seen in
    the training set, while having similar relative frequencies of the lemmas and dependency
    relation tags (= elements of the compound tuples = atoms).
    """

    def evaluate_predictions(
        self,
        *,
        predictions: List[Mapping[str, Any]] = None,
        gold: Dataset = None,
    ) -> EvaluationResult:
        result = OrderedDict()
        for metric_config in self.config.evaluation_metrics:
            hf_id = metric_config.hf_id
            if isinstance(hf_id, str):
                hf_id = [hf_id]

            metric = evaluate.load(*hf_id, revision=metric_config.git_commit_sha)

            refs_lst = [g["target"] for g in gold]
            preds_lst = [pred["target"] for pred in predictions]

            ref_type = type(refs_lst[0])
            pred_type = type(preds_lst[0])
            if pred_type != ref_type:
                if self.config.task_type != TaskType.MULTIPLE_CHOICE:
                    raise ValueError(
                        f"Predictions and references have different types: preds: {pred_type} and refs: {ref_type}. "
                    )
                # Convert predictions to the same type as the references
                if pred_type == str and ref_type == int:
                    logger.warning("Predictions are strings, but references are ints. Converting predictions to ints.")
                    converted_preds = []
                    for pred, ref in zip(preds_lst, gold):
                        assert "target_options" in ref
                        converted_preds.append(ref["target_options"].index(pred))
                    preds_lst = converted_preds
                elif pred_type == int and ref_type == str:
                    logger.warning("Predictions are ints, but references are strings. Converting references to ints.")
                    converted_refs = []
                    for pred, ref in zip(preds_lst, gold):
                        assert "target_options" in ref
                        converted_refs.append(ref["target_options"].index(ref["target"]))
                    refs_lst = converted_refs
            else:
                if self.config.task_type == TaskType.MULTIPLE_CHOICE and pred_type != int:
                    # Convert both predictions and references to int
                    logger.warning(
                        "Predictions and references have the same type, but it is not int. Converting both to int."
                    )
                    converted_preds = []
                    converted_refs = []
                    for pred, ref in zip(preds_lst, gold):
                        assert "target_options" in ref
                        converted_preds.append(ref["target_options"].index(pred))
                        converted_refs.append(ref["target_options"].index(ref["target"]))
                    preds_lst = converted_preds
                    refs_lst = converted_refs

            extra_kwargs = metric_config.compute_extra_kwargs or {}
            output: dict = metric.compute(predictions=preds_lst, references=refs_lst, **extra_kwargs)

            if output is None:
                raise ValueError(
                    f"Metric {metric_config.hf_id} returned None. " f"Please check the metric implementation."
                )

            # Update output keys to include the metric id
            metric_id = "_".join(hf_id)
            output = {f"hf_{metric_id}__{k}": v for k, v in output.items() if k == "score"}

            result.update(output)

        return result

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
