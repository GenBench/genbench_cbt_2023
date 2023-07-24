# Shifted Pauq (en_pauq_iid_split)

## Abstract
This is original split from Spider dataset in English. 

## Examples
```
{'id': 'TS_0014',
 'db_id': 'department_management',
 'source': 'spider-train',
 'type': 'train',
 'query': "SELECT T3.born_state FROM department AS T1 JOIN management AS T2 ON T1.department_id  =  T2.department_id JOIN head AS T3 ON T2.head_id  =  T3.head_id WHERE T1.name  =  'Treasury' INTERSECT SELECT T3.born_state FROM department AS T1 JOIN management AS T2 ON T1.department_id  =  T2.department_id JOIN head AS T3 ON T2.head_id  =  T3.head_id WHERE T1.name  =  'Homeland Security';",
 'question': "List the states where both the secretary of 'Treasury' department and the secretary of 'Homeland Security' were born.",
 'sql': {'from': {'table_units': [['table_unit', 0],
    ['table_unit', 2],
    ['table_unit', 1]],
   'conds': [[False, 2, [0, [0, 1, False], None], [0, 11, False], None],
    'and',
    [False, 2, [0, [0, 12, False], None], [0, 7, False], None]]},
  'select': [False, [[0, [0, [0, 9, False], None]]]],
  'where': [[False, 2, [0, [0, 2, False], None], '"Treasury"', None]],
  'groupBy': [],
  'having': [],
  'orderBy': [],
  ...},
 'question_toks': ['List',
  'the',
  'states',
  'where',
  'both',
  'the',
  'secretary',
  ...],
 'query_toks': ['select',
  't3.born_state',
  'from',
  'department',
  'as',
  't1',
   ...],
 'query_toks_no_values': ['select',
  't3.born_state',
  'from',
  'department',
  ...],
 'masked_query': 'SELECT T3.born_state FROM department AS T1 JOIN management AS T2 ON T1.department_id = T2.department_id JOIN head AS T3 ON T2.head_id = T3.head_id WHERE T1.name = TEXT_VALUE_1 INTERSECT SELECT T3.born_state FROM department AS T1 JOIN management AS T2 ON T1.department_id = T2.department_id JOIN head AS T3 ON T2.head_id = T3.head_id WHERE T1.name = TEXT_VALUE_2'}
```

## Usage
*Describe how to load your task and what is required for evaluation, if anything.*

## Data Source
*Describe the data source for this Shifted Pauq (en_pauq_iid_split).*

## Limitations and Bias
*Note any known limitations or biases that the Shifted Pauq (en_pauq_iid_split) has, with links and references if possible.*

## GenBench Eval card
*Describe what kind of generalisation your task is evaluating, and include a [genbench eval card](https://genbench.org/eval_cards/) for your task*.
