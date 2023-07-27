# Shifted PAUQ -- Text-to-SQL (ru_pauq_iid_split)

## Abstract
This is an original split of the Russian _Text-to-SQL_ dataset, PAUQ [1], which is under the assumption of independency and identically (i.i.d) distributed train and test data. We provide this split in addition to the **ru_pauq_target_length_split** split.

PAUQ is the Russian version of the Spider, where all three components have been modified and localized: the natural language (NL) questions, the SQL queries, and the content of the databases. 

From PAUQ abstract [1]: We construct and complement a Spider dataset for the Russian language, thus creating the first publicly available text-to-SQL dataset in Russian. While examining dataset components—NL questions, SQL queries, and database content—we identify limitations of the existing database structure, fill out missing values for tables and add new requests for underrepresented categories. To conduct the experiment, we adapt baseline models RAT-SQL and BRIDGE and provide in-depth query component analysis. Both models demonstrate strong single language results and improved accuracy with multilingual training on the target language.

baseline scores of a sequence-to-sequence model such as BRIDGE: please refer to [1] for details

the size of the dataset: please refer to [1] for details

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

Train/test data for the ru_pauq_iid split is available at https://huggingface.co/datasets/composite/pauq/viewer/ru_pauq_iid

## Limitations and Bias
*Note any known limitations or biases that the Shifted Pauq (ru_pauq_target_length_split) has, with links and references if possible.*

from [1]: PAUQ is an adaptation of the Spider dataset to Russian language, it indeed inherits most of Spider's limitations. First of all, the data is still `artificial' which means that it was created by a limited number of people specifically for training and evaluating text-to-SQL models, thus it lacks the diversity and complexity of natural data formed by questions that people formulate in order to get the desired information from the database. For instance, the real-world data contain NL queries that require common sense knowledge which can't be extracted directly from the database; ambiguous questions allowing various ways of interpretation that are quite frequent and queries with window functions that make the process easier and more convenient, -- all of these aren't included in the Spider dataset, as well as in PAUQ. Another limitation concerns evaluation metric -- exact match, which is the most commonly used to evaluate text-to-SQL models performance. However, the metric is too strict and prone to false negative results.


## GenBench Eval card
*Describe what kind of generalisation your task is evaluating, and include a [genbench eval card](https://genbench.org/eval_cards/) for your task*.

**GenBench taxonomy values for the experiments:**

Motivation: Practical

Generalisation type: Compositional, Structural

Shift type: Covariate

Shift source: Naturally occuring

Shift locus: train--test, Finetune train--test

