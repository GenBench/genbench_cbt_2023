from collections import OrderedDict
from typing import Any, Dict, List, Mapping

import evaluate
from datasets import Dataset

from genbench import Task
from genbench.api import EvaluationResult, TaskType
from genbench.utils.logging import get_logger


logger = get_logger(__name__)


def make_list(N, ind_1):
    binary_list = [0] * N
    binary_list[ind_1] = 1
    return binary_list


class BlmTasksAltAtl(Task):
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

                    N = len(ref["target_options"])

                    converted_preds = []
                    converted_refs = []
                    for pred, ref in zip(preds_lst, gold):
                        assert "target_options" in ref
                        # converted_preds.append(ref["target_options"].index(pred))
                        # converted_refs.append(ref["target_options"].index(ref["target"]))

                        converted_preds.extend(make_list(N, ref["target_options"].index(pred)))
                        converted_refs.append(make_list(N, ref["target_options"].index(ref["target"])))

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
            output = {f"hf_{metric_id}__{k}": v for k, v in output.items()}

            result.update(output)

        return result

    def format_example(self, example: Dict[str, Any]) -> Dict[str, Any]:
        """Perform preprocessing/formatting on an example-level.

        By default, this method does nothing more than mapping original data source
        fields to the expected fields.

        `example` directly comes from the data source (e.g. downloaded HF dataset),
        and it may contain fields such as `question` or `answer`. This method should
        prepare the example used in the task. i.e. should create fields `input`,
        `target`, `target_scores`, or `target_labels` depending on the task type.

        Args:
            example: A dictionary containing key-value pairs for an example from the source dataset.


        Returns:
            A dictionary containing key-value pairs for the preprocessed/formatted example.
            The dictionary should contain keys `input`, `target`, `target_scores`, or `target_label`
            depending on the task type.
        """
        return {"input": example["input"], "target": example["target"], "target_options": example["target_options"]}
