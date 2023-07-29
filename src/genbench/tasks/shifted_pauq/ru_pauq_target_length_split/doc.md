# Shifted PAUQ -- Text-to-SQL (ru_pauq_target_length_split)
*A brief explaination of the task, its motivation and a description of the submssion data. Minimally, this should include: what generalisation property(ies) the task is testing for (GenBench taxonomy values); what assumptions are made about the training data; the size of the dataset; baseline scores. If it already contains this information, feel free to copy the abstract of the accompanying paper.*

## Abstract
In this work, we propose a custom split of the Russian _Text-to-SQL_ dataset, PAUQ [1], that assesses compositional generalization in a _text-to-query_ models. 
The proposed split, ru_pauq_target_length_split, is length-based split based on the token length, i.e. datasets' items are separated by length such that the test set contains examples of different lengths than those in the train set. In this setup, we measure generalization to more complex queries.
Dataset is split between train and test based on 30th percentile.
In order to measure compositional generalization, we have verified that all SQL test tokens are present in train.

* Baseline scores of a sequence-to-sequence model: TODO
* The size of the dataset: please refer to [1] for details
* The size of the split: TODO

## Examples
```
{'id': 'TS_0014',
 'db_id': 'department_management',
 'source': 'spider-train',
 'type': 'train',
 'query': "SELECT T3.born_state FROM department AS T1 JOIN management AS T2 ON T1.department_id  =  T2.department_id JOIN head AS T3 ON T2.head_id  =  T3.head_id WHERE T1.name  =  'Управление общего учёта' INTERSECT SELECT T3.born_state FROM department AS T1 JOIN management AS T2 ON T1.department_id  =  T2.department_id JOIN head AS T3 ON T2.head_id  =  T3.head_id WHERE T1.name  =  'Бюджетная служба Конгресса';",
 'question': 'Перечислите штаты, в которых родились и секретарь управления общего учёта, и секретарь бюджетной службы Конгресса.',
 'sql': {'from': {'table_units': [['table_unit', 0],
    ['table_unit', 2],
    ['table_unit', 1]],
   'conds': [[False, 2, [0, [0, 1, False], None], [0, 11, False], None],
    'and',
    [False, 2, [0, [0, 12, False], None], [0, 7, False], None]]},
  'select': [False, [[0, [0, [0, 9, False], None]]]],
  'where': [[False,
    2,
    [0, [0, 2, False], None],
    '"Управление общего учёта"',
    None]],
  'groupBy': [],
  'having': [],
  'orderBy': [],
  'limit': None,
  'intersect': {'from': {'table_units': [['table_unit', 0],
     ['table_unit', 2],
     ['table_unit', 1]],
    'conds': [[False, 2, [0, [0, 1, False], None], [0, 11, False], None],
     'and',
     [False, 2, [0, [0, 12, False], None], [0, 7, False], None]]},
   'select': [False, [[0, [0, [0, 9, False], None]]]],
   'where': [[False,
     2,
     [0, [0, 2, False], None],
     '"Бюджетная служба Конгресса"',
     None]],
  ...},
 'question_toks': ['Перечислите',
  'штаты',
  ',',
  'в',
  'которых',
  'родились',
  ...],
 'query_toks': ['select',
  't3.born_state',
  'from',
  'department',
  'as',
  't1',
  'join',
  'management',
  ...],
 'query_toks_no_values': ['select',
  't3.born_state',
  'from',
  'department',
  'as',
  't1',
  'join',
  ...],
 'masked_query': 'SELECT T3.born_state FROM department AS T1 JOIN management AS T2 ON T1.department_id = T2.department_id JOIN head AS T3 ON T2.head_id = T3.head_id WHERE T1.name = TEXT_VALUE_1 INTERSECT SELECT T3.born_state FROM department AS T1 JOIN management AS T2 ON T1.department_id = T2.department_id JOIN head AS T3 ON T2.head_id = T3.head_id WHERE T1.name = TEXT_VALUE_2'}
```

## Usage
*Describe how to load your task and what is required for evaluation, if anything.*

For evaluation, we will use a sequence-to-sequence architecture. Evaluation metric is exact match. Please refer to config.jsonnet for details for now.


## Data Source
*Describe the data source for this Shifted Pauq (ru_pauq_target_length_split).*

The PAUQ statistics can be found in [1]

Train/test data for the ru_pauq_target_length_split split is available at https://huggingface.co/datasets/composite/pauq/viewer/ru_pauq_tl

## Limitations and Bias
*Note any known limitations or biases that the Shifted Pauq (ru_pauq_target_length_split) has, with links and references if possible.*

Our research explores distribution shift, i.e. spurious correlation using ru_pauq_target_length_split, and investigates how they affect the model. Specifically, we examine the scenario where test tokens are present in the training set and do not explore the more challenging case of modeling unseen tokens.

Another limitation concerns evaluation metric -- exact match, which is the most commonly used to evaluate text-to-SQL models performance. However, this metric is too strict and prone to false negative results [1].

Big language models such as Codex, a 175B GPT model further fine-tuned on code, are out of the scope of this study.

## GenBench Eval card
*Describe what kind of generalisation your task is evaluating, and include a [genbench eval card](https://genbench.org/eval_cards/) for your task*.

### GenBench taxonomy values for the experiments:

* **Motivation:** Practical
* **Generalisation type:** Compositional, Structural
* **Shift type:** Covariate
* **Shift source:** Naturally occuring
* **Shift locus:** train--test, Finetune train--test


## References
[1] PAUQ: Text-to-SQL in Russian
```
@inproceedings{pauq,
  title={PAUQ: Text-to-SQL in Russian},
  author={Bakshandaeva, Daria and Somov, Oleg and Dmitrieva, Ekaterina and Davydova, Vera and Tutubalina, Elena},
  booktitle={Findings of the Association for Computational Linguistics: EMNLP 2022},
  pages={2355--2376},
  year={2022}
}
```
