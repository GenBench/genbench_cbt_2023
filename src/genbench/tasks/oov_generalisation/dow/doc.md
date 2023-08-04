# OOV Generalisation (dow)

## Abstract
Subword tokenization is fundamental preprocessing step for all SOTA LMs, and is designed to avoid Out-Of-Vocabulary (OOV) issues by segmenting OOV words into subwords. However, the NLP community has no formal downstream task for evaluating SOTA subword tokenizers. So that, in this gap, we propose OOV Generalisation Challenge for testing OOV issues. This challenge has three subtasks: Definition of Word (DoW), Word and Word (WaW), Morphology of Word (MoW)

## Examples
Subtask 1:
Classify if word and definition matches: True or False?

Input: W: liter D: a metric unit of capacity equal to the volume of 1 kilogram of pure water at 4 degrees centigrade and 760 mm of mercury (or approximately 1.76 pints)
Output: True

Input: W: designed D: a carpenter's plane intermediate between a jack plane and a jointer plane
Output: False

## Usage
*Describe how to load your task and what is required for evaluation, if anything.*

## Data Source
TBW

## Limitations and Bias
*Note any known limitations or biases that the OOV Generalisation (dow) has, with links and references if possible.*

## GenBench Eval card
This subtask has a practical motivation, evaluating compositional generalisation under generated covariate shifts between finetuning and test stages. 
