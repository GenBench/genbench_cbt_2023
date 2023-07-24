# Shifted Pauq (ru_pauq_target_length_split)

## Abstract
This is length based split based on the token length of target query in Russian. Dataset is split between train and test based 
on 30th percentile. In order to measure compositional generalization we have verified that all SQL test tokens are present in train.

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

## Data Source
*Describe the data source for this Shifted Pauq (ru_pauq_target_length_split).*

## Limitations and Bias
*Note any known limitations or biases that the Shifted Pauq (ru_pauq_target_length_split) has, with links and references if possible.*

## GenBench Eval card
*Describe what kind of generalisation your task is evaluating, and include a [genbench eval card](https://genbench.org/eval_cards/) for your task*.
