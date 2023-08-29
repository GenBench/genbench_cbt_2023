# PromptComVE

## Motivation
Recently, zero- and few-shot learning with various prompt-based, Instruction-tuned Large Language Models (It-LLMs) have made extraordinary progress. Indeed, prompts seem to help models learn faster, just as humans learn faster when they receive task instructions expressed in natural language. However, these models often produce good predictions with meaningless, irrelevant and misleading prompts, even at zero-shots. This resource propose a benchmark to probe generalization abilities over commonsese reasoning task. Hence, inspired by the Commonsense Validation and Explanation (ComVE), through a systematic analysis, we analyzed several It-LLMs, in particular, whether they are able to distinguish statements that make sense from those that do not by providing comprehensive explanations. Thus, we show that It-LLMs have good generalization abilities and achieve good accuracy in commonsense reasoning tasks. However, despite the impressive performance and improvements, we found some weaknesses that cast doubt on whether the models improved understanding of task instructions in a similar way to humans' use of task instructions.

## Examples
**match**: {"input": "Which of the two statements is impossible? a)he put an elephant into the fridge. b)he put a turkey into the fridge", "target": "a)"}


## GenBench Eval card
*Describe what kind of generalisation your task is evaluating, and include a [genbench eval card](https://genbench.org/eval_cards/) for your task*.
