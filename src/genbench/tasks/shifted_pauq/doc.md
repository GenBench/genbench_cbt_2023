## Motivation
Shifted Pauq is an update of Spider dataset. We have fixed the original queries and database content. 
We have also translated both questions and queries to Russian language and updated database content with Russian entities.
In this evaluation we want to explore the ability of finetuned language models to cope with distribution shift 
in a field of semantic parsing on different generated splits - target query length, 
target maximum compound divergence(will be submitted later) in contrast to i.i.d. generated split. 

## Examples
Each sample follows the original Spider structure.
**English example**
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

**Russian example**

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

Each query is supported by a corresponding database for measuring execution match.

## Data Source
Originaly Spider was annotated by 11 Yale students. In our work we have refined it and translated with experts help.

## Limitations and Bias
*Note any known limitations or biases that the Shifted Pauq has, with links and references if possible.*

## Citation
[https://aclanthology.org/2022.findings-emnlp.175.pdf](https://aclanthology.org/2022.findings-emnlp.175.pdf)
```
@inproceedings{bakshandaeva-etal-2022-pauq,
    title = "{PAUQ}: Text-to-{SQL} in {R}ussian",
    author = "Bakshandaeva, Daria  and
      Somov, Oleg  and
      Dmitrieva, Ekaterina  and
      Davydova, Vera  and
      Tutubalina, Elena",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2022",
    month = dec,
    year = "2022",
    address = "Abu Dhabi, United Arab Emirates",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.findings-emnlp.175",
    pages = "2355--2376",
    abstract = "Semantic parsing is an important task that allows to democratize human-computer interaction. One of the most popular text-to-SQL datasets with complex and diverse natural language (NL) questions and SQL queries is Spider. We construct and complement a Spider dataset for Russian, thus creating the first publicly available text-to-SQL dataset for this language. While examining its components - NL questions, SQL queries and databases content - we identify limitations of the existing database structure, fill out missing values for tables and add new requests for underrepresented categories. We select thirty functional test sets with different features that can be used for the evaluation of neural models{'} abilities. To conduct the experiments, we adapt baseline architectures RAT-SQL and BRIDGE and provide in-depth query component analysis. On the target language, both models demonstrate strong results with monolingual training and improved accuracy in multilingual scenario. In this paper, we also study trade-offs between machine-translated and manually-created NL queries. At present, Russian text-to-SQL is lacking in datasets as well as trained models, and we view this work as an important step towards filling this gap.",
}
```

## Further References
*Add any useful further references.*