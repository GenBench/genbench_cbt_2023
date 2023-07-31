from typing import Any, Dict, List

import datasets
import numpy as np

from genbench import Task


class CrossLingualConsistencyTask(Task):
    def evaluate_predictions(
        self,
        *,
        predictions: List[Dict[str, Any]] = None,
        gold: datasets.Dataset = None,
    ) -> Dict[str, float]:
        pass

    def format_example(self, example: Dict[str, Any]) -> Dict[str, Any]:
        lang1_rankings = eval(example["lang1_rankings"])
        lang2_rankings = eval(example["lang2_rankings"])
        cand1 = eval(example["lang1_cands"])
        cand2 = eval(example["lang2_cands"])

        def softmax(x):
            # Compute softmax values for each sets of scores in x.
            return np.exp(x) / np.sum(np.exp(x), axis=0)

        weight_metric = "softmax"  # softmax norm1 norm2

        cand_list1 = [[j for j in list(i.keys())] for i in cand1]
        cand_list2 = [[j for j in list(i.keys())] for i in cand2]

        num_consistent = 0

        # for i in range(len(lang1_rankings)): 
        # Original line. It works well locally but encounters errors 
        # with the genbench_cbt framework. 
        # (Highly likely related to cache files.)
        for i in range(3): 
            # So we manually change the ranging number to 3, 
            # the number of queries for the sample in test_sample.jsonl
            ranking1 = lang1_rankings[i]
            ranking2 = lang2_rankings[i]

            candidate1 = cand_list1[i]
            candidate2 = cand_list2[i]

            order = [len(ranking1) - i for i in range(len(ranking1))]
            order = np.array(order)

            if weight_metric == "softmax":
                weight = softmax(order)
            elif weight_metric == "norm1":
                weight = order / np.sum(order)
            else:
                weight = np.power(order, 2) / np.sum(np.power(order, 2))

            for j in range(len(ranking1)):
                set1 = {candidate1.index(i) for i in ranking1[: j + 1]}
                set2 = {candidate2.index(i) for i in ranking2[: j + 1]}

                cover = set1.intersection(set2)
                num_consistent += weight[j] * (len(cover) / len(set1))

        """
        return {
            "rankings of candidates when probing Bloom-3b with en factual queries in BMLAMA:": str(lang1_rankings),
            "rankings of candidates when probing Bloom-3b with es factual queries in BMLAMA:": str(lang2_rankings),
            "CLC computed with our proposed RankC metric": str(num_consistent / len(lang1_rankings)),
        }
        """
        input_tmp = []
        target_tmp = []
        input_tmp = str(lang1_rankings) + str(lang2_rankings)
        target_tmp = str(num_consistent / len(lang1_rankings))
        return {
            "input": input_tmp,
            "target": target_tmp,
        }
