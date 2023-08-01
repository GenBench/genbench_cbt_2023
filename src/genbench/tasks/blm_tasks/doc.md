## Motivation
When exposed to tests of analytic intelligence, for example the visual RAVEN IQ test, human problem-solvers identify the relevant objects in the picture and their relevant attributes and reason based on rules applied to these objects and attributes. Based on the induced rules, they are able to provide a solution to the test.

The tasks we propose translate this IQ task into language. Each subtask pertains to a grammatical or linguistic phenomenon, and the corresponding dataset consists of a sequence of sentences. The sentence structure is constructed to illustrate several underlying generative rules that describe different aspects of the linguistic phenomenon. These rules need to be identified and disentangled to correctly generalize and thus identify the correct answer. The sequence structure was designed in a similar manner to visual IQ tests, and follows a generative process of overlapping rules. The output is multiple choice. The correct sentence should be the correct continuation of the input sequence w.r.t. the dataset's generation rules.

## Examples
We have three subtasks:

* `agrF`: subject-verb agreement in French:

Input: 

|---|-----------|------------------|-----------------|--------|
| 1 | The vase  | with the flower  |                 | leaks. |
| 2 | The vases | with the flower  |                 | leak.  |
| 3 | The vase  | with the flowers |                 | leaks. |
| 4 | The vases | with the flowers |                 | leak.  |
| 5 | The vase  | with the flower  | from the garden | leaks. |
| 6 | The vases | with the flower  | from the garden | leak.  |
| 7 | The vase  | with the flowers | from the garden | leaks. |
| 8 | ???       |

Choices:

|                                                           |         |
|-----------------------------------------------------------|---------|
| The vase with the flower  and the garden  leaks.          | Coord   |
| extbf{The vases with the flowers  from the garden  leak.} | Correct |
| The vase with the flower   leaks.                         | WNA     |
| The vase with the flower   from the garden  leak.         | AE      |
| The vases with the flower  from the garden  leak.         | WN1     |
| The vases with the flowers  from the gardens  leak.       | WN2     |
|-----------------------------------------------------------|---------|

* `ALT-ATL`: spray/load verb alternation in English (from Agent - Locative - Theme to Agent - Theme - Locative)

Input:

|   |                                                 |
|---|-------------------------------------------------|
| 1 | The girl sprayed the wall with paint.           |
| 2 | Paint was sprayed by the girl                   |
| 3 | Paint was sprayed onto the wall by the girl     |
| 4 | Paint was sprayed onto the wall                 |
| 5 | The wall was sprayed by the girl                |
| 6 | The wall was sprayed with the paint by the girl |
| 7 | The wall was sprayed with paint                 |
| 8 | ???                                             |

Choices:

|                                           |          |
|-------------------------------------------|----------|
| The girl sprayed paint onto the wall      | Correct  |
| The girl was sprayed paint onto the wall  | AgentAct |
| The girl sprayed paint the wall           | Alt1     |
| The girl sprayed with paint onto the wall | Alt2     |
| The girl sprayed paint for the room       | NoEmb    |
| The girl sprayed paint under the wall     | LexPrep  |
| Paint sprayed the girl onto the wall      | SSM      |
| The wall sprayed the girl with paint      | SSM      |
| Paint sprayed the wall with the girl      | AASSM    |


* `ATL-ALT`: verb causal alternation in English (from Agent - Theme - Locative to Agent - Locative - Theme)


## Data Source
All datasets are automatically generated based on manually selected seeds and predefined (syntactic) templates.

## Limitations and Bias
The sentences and the sequence of sentences for each dataset have a prescribed structure. Each dataset is focused on one specific phenomenon.

## Citation

[BLM-AgrF: A New French Benchmark to Investigate Generalization of Agreement in Neural Networks](https://aclanthology.org/2023.eacl-main.99/) describes the BLM_AgrF dataset -- subject-verb agreement in French.


## Further References

[Blackbird's language matrices (BLMs): a new benchmark to investigate disentangled generalisation in neural networks](https://arxiv.org/abs/2205.10866) describes the project, and the first BLM dataset generated within this paradigm.

[Blackbird language matrices (BLM), a new task for rule-like generalization in neural networks: Motivations and Formal Specifications](https://arxiv.org/abs/2306.11444) provides details about the motivations and formal specifications of BLM's.