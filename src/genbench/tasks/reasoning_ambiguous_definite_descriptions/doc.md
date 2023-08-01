# Reasoning about Ambiguous Definite Descriptions

## Abstract
Natural language reasoning plays an increasingly important role in improving language models' ability to solve complex language understanding tasks.
An interesting use case for reasoning is the resolution of context-dependent ambiguity.
But no resources exist to evaluate how well Large Language Models can use explicit reasoning to resolve ambiguity in language.
We propose to use ambiguous definite descriptions for this purpose and create and publish the first benchmark dataset consisting of such phrases.
Our method includes all information required to resolve the ambiguity in the prompt, which means a model does not require anything but reasoning to do well.

## Examples
|          | Component           | Explanation                                                                                                                  | Example                                                                                                                                                                         |
|----------|---------------------|------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Premises | entity-relations    | A number of relations of the entity and the context in which it is true.                                                     | Lars Lervik was part of the Telemark Battalion from January 2010 to January 2013.  <br/> Lars Lervik was part of the Brigade Nord from January 2018 to January 2020.            | 
|          | relation-properties | The value of the property for each relation.                                                                                 | Brigade Nord is a military unit of size class brigade.  <br/> Telemark Battalion is a military unit of size class battalion.                                                    |
|          | regularity          | The relevant rule or regularity that is required to resolve the ambiguity.                                                   | Military units do not change size class.                                                                                                                                        |
| Question | context             | Establishes the current context.                                                                                             | If the current date is June 2019                                                                                                                                                |
|          | sentence            | An ambiguous sentence with a temporal operator and a property being ascribed to an entity denoted by a definite description. | what is the most likely interpretation of the following sentence: <br/> The military unit of Lars Lervik was of size class brigade in March 2010.                               |
|          | interpretations     | Two interpretations for the ambiguous sentence, one of which contradicts the regularity.                                     | 1. Lars Lervik's unit in March 2010 (Telemark Battalion) was of size class brigade. <br/> 2. Lars Lervik's current unit (Brigade Nord) was of size class brigade in March 2010. |

## Usage
*Describe how to load your task and what is required for evaluation, if anything.*

## Data Source
*Describe the data source for this reasoning_ambiguous_definite_descriptions.*

## Limitations and Bias
*Note any known limitations or biases that the reasoning_ambiguous_definite_descriptions has, with links and references if possible.*

## GenBench Eval card
*Describe what kind of generalisation your task is evaluating, and include a [genbench eval card](https://genbench.org/eval_cards/) for your task*.
