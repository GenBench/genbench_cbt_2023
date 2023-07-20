# ICL consistency test

## Abstract
Finding the best way of adapting pre-trained language models to a task is a big challenge in current NLP.
Just like the previous generation of task-tuned models (TT), models that are adapted to tasks via in-context-learning (ICL) or instruction tuning (IT) are robust in some setups, but not in others.
Here, we present a detailed analysis of which design choices cause instabilities and inconsistencies in LLM predictions.
First, we show how spurious correlations between input distributions and labels -- a known issue in TT  models -- form only a minor problem for prompted models.
Then we engage in a systematic, holistic evaluation of different factors that have been found to influence predictions in a prompting setup.
We test all possible combinations of a range of factors on both vanilla and instruction-tuned LLMs of different scale, and statistically analyse the results to show which factors are the most influential, the most interactive or the most stable.
From our results, we deduce which factors can be used without precautions, should be avoided or handled with care in most settings.

## Examples
*Give some examples of the ICL consistency test.*

## Usage
#### Dataloading
The task can loaded through the default GenBench interface as a zero-shot task:
```python
from genbench import load_task
from genbench.api import PreparationStrategy

task = load_task("icl_consistency_test")
ds = task.get_prepared_datasets(
                    PreparationStrategy.PROMPT_BASED_TESTING, 
                    shot_list=[0]
                    )[0]
```
#### Evaluation
Provide the evaluation function with the model outputs as strings, accompanied by the corresponding setup-ids and data-ids 
from the original dataset.
For the predictions, please follow the following format: 

`predictions: Dict[setup_ID, Dict[data_ID, model_output]]`

For the gold labels, please provide the original dataset ds:

`gold: datasets.Dataset`

With this input, run the task evaluation like so:
```python
results = task.evaluate_predictions(predictions=predictions, 
                                    gold=ds)
```

## Data Source
The original data stems from the ANLI dataset (Nie et al., 2019).

## Limitations and Bias
- the number of factors in limited and does not cover all possible factors that might influence the predictions
- currently only works for ANLI
- factors such as _Instruction tuning_ or _calibration_ are dependent of the model inference process (Which model is evaluated? How is it evalauted?) These factors have to be manually added by the user. 

*Note any known limitations or biases that the ICL consistency test has, with links and references if possible.*

## GenBench Eval card
- The task is evaluating the consistency of LLM predictions across different setups. It evaluates to which degree predictions change if we change certain factors in the prompt design.


[Genbench Eval Card](GenBench_eval_card.pdf)

## References

Nie, Y., Williams, A., Dinan, E., Bansal, M., Weston, J., & Kiela, D. (2019). Adversarial NLI: A new benchmark for natural language understanding. arXiv preprint arXiv:1910.14599.