# GenBench Collaborative Benchmarking Task

## Implementation Status
| Task | Status |
| --- |--------|
| CLI Create New Task | Done   |
| Task Class Implementation | In Progress |

### CLI Create New Task
```bash
pip install -e .
```
Use `genbench-cli` to create a new task. Use `genbench-cli create-task --help` for more information.
```bash
genbench-cli create-task --task-name "My Awesome Task"
```

**NB: This repository describes how tasks can be submitted, but submissions are not open yet.
Submissions are expected to open on June 7.**

**Table of Contents**
* [GenBench workshop and publication of tasks](#genbench-workshop-and-publication-of-tasks)
* [How to submit a task to the GenBench CBT](#how-to-submit-a-task-to-the-genbench-cbt)
    * [Overview](#overview)
    * [Task](#task)
    * [Task types](#task-types)
    * [Task files](#task-files)
        * [`config.jsonnet`](#configjsonnet)
        * [`task.py`](#taskpy)
        * [`split.jsonnet` (Optional)](#splitjsonnet)
        * [`doc.md`](#docmd)
    * [Manual data source](#manual-data-sources)
* [Most Common Use Cases (Examples)](#most-common-use-cases-examples)
    * [Train-Test (finetuning)](#train-test-finetuning)
    * [Prompt-based testing](https://github.com/GenBench/genbench_cbt/tree/main#prompt-based-testing)
    * [Custom Task Examples](https://github.com/GenBench/genbench_cbt/tree/main#custom-taskpy-examples)
      * [Custom Metric/Evaluation](#custom-metricevaluation-metric)
      * [Custom Example Formatting/Pre-processing](#custom-example-formattingpre-processing)
      * [Custom Dataset Preparation Loop](#custom-dataset-preparation-loop)

## GenBench Workshop and Publication of Tasks
The Genbench Collaborative Benchmarking Task (CBT) aims to develop a collaborative generalisation benchmark for NLP, hosted on a shared platform: GenBench.
Submissions to the CBT consist of a data/task artefact (submitted via this repository) and a paper (submitted via openreview), describing the submission. Tasks will be reviewed via their paper submission, and tasks from accepted papers will be merged into the repository. After the workshop, we will release a leaderboard for the top-reviewed tasks.

You can find more details about the GenBench program, the workshop and the task, on our website https://genbench.org/workshop.

## How to submit a task to the GenBench CBT
**NB:** We are currently working on a CLI tool that will automate a lot of the steps in the submssions process, including stub generation, formatting, validation, testing, and model evaluation. 
Once the tool is publicly available, we will update the following instructions.

### Overview
1. **Fork the [`genbench/genbench_cbt`](https://github.com/GenBench/genbench) repository.**

2. **Create a branch on the forked repo, e.g. `my_awesome_task`.**

3. **Clone the repo**
```bash
git clone https://github.com/awesome-task-creator/genbench_cbt
cd genbench
git checkout -b my_awesome_task
```
Your clone repo will contain the following files:
```
- repo/
  - genbench/
    - tasks/
      - sample_task/
        - __init__.py
        - config.jsonnet
        - task.py
        - doc.md
      ...
```
5. **Create a new task from the sample**
Copy the `sample_task` directory to a new one with your task's name:
```
cd genbench/tasks
cp -r sample_task my_awesome_task
```
Alternatively, simply create a new directory with two files: `config.jsonnet`, and `doc.md`.

6. **Configure your task**
You will need to fill in `config.jsonnet`, and if necessary `task.py`.
See below for further instructions and details about these two files.

7. **Push the new changes to your fork**
```bash
git add genbench/tasks/my_awesome_task/*
git commit -m "Add My Awesome Task"
git push --set-upstream origin my_awesome_task
```

8. **Commit, Push and Submit a pull request to GenBench**
```
git commit -m "Submission for my_awesome_task"
git push
```
### Task
A GenBench task involves providing a test set along with optional train and validation sets. Each set is comprised of a collection of examples, where each example is represented as a dictionary containing the input and the corresponding ground truth output.

We offer complete flexibility in terms of how these examples are prepared and how the model's predictions are evaluated. This allows for the creation of diverse and varied benchmarking that can be tailored to the needs of specific generalization protocols.


### Task Types
The submitted benchmark tasks can be one of the following three different types: Sequence Classification, Sequence Labeling, and Free-form Generation. The choice of type will dictate various parts of the submission, like the choice of evaluation metrics, dataset field mapping and model preparation (see the [config](#configjsonnet) section).
In the following list we provide an examples of data instances for each task type.

#### Addition (Free-form Generation)
```json
{
    "input": "300 + 80", 
    "target": "380"
}
```
The `input` and `target` are both strings. Given the input the model has to generate an answer. The task creator can specify how the generation is performed (e.g. sampling method or stop string) in the config file. Note that encoder-only models such as RoBERTa do not support this task type.

#### SNLI (Multi-choice Classification)
```json
{
   "input": "P: A man inspects the uniform of a figure in some East Asian country. H: The man is sleeping",
   "target": 1,
   "target_options": ["Entailment", "Contradiction", "Neutral"]
}
```
The `input` is a string and `target` is the label index.

#### Knowledge QA (Multi-choice Classification)
```json
{
   "input": "Who was the first president of the United States?",
   "target": 0,
   "target_options": [
        "George Washington",
        "Barack Obama",
        "Michael Jackson",
        "None of the above",
   ]
}
```
The `target_options` can change per each data instance.

#### NER (Sequence Labeling)
```json
{
    "input": ["Steve", "Jobs", "was", "a", "CEO", "at", "Apple."],
    "target": ["B-person", "I-person", "O", "O", "O", "O", "B-corporation"],
}
```
Both `input` and `target` are a list of strings with the same size.



### Task files
The GenBench APIs are designed to reduce the burden of coding from task creators as much as possible but also allow a lot of flexibility. 

To this end, GenBench tasks exist as Python classes and are defined using two files: `config.jsonnet` and the task's class defined in `task.py`. `config.jsonnet` essentially configures the task object and behaviour. In most common use-cases, the `.jsonnet` file should provide sufficient flexibility for task creators so that they can define their task without any coding. However, in case even more flexibility is needed, there are a battery of methods inside the Python class that can customize the behaviour of the task.

#### `config.jsonnet`
*Jsonnet (https://jsonnet.org) is a superset of JSON (json+added functionalities). So, every `.json` file is already a `.jsonnet file`.*
```jsonnet
{
    name: 'My Awesome Task',
    description: 'Some short description of it',

    // We recommend you use the GenBench taxonomy values that describe your task as keywords. 
    // You can copy them from your GenBench Evaluation Card (https://genbench.org/eval_cards/)
    keywords: [
        'Keyword1',
        'Keyword2',
    ],

    authors: [
        'Author1',
        'Author2',
    ],


    // We allow submissions involving HuggingFace datasets or publicly accessible URIs to
    // dataset files hosted with a date stamp (only one option is allowed).
    //
    // As the data source examples can have any number of fields, you need to declare
    // which ones are required for the task using the `field_mapping` attribute below,
    // or the `format_example(...) of the Python class

    // Option 1 (delete if not needed): Use a HuggingFace dataset
    data_source: {
        type: 'hf',
        
        // Huggingface datasets ID
        hf_id: 'snli', // or ['super_glue', 'MultiRC'] in case of datasests that are part of benchmarks
        
        // To ensure the HF dataset is read from the same version 
        // every time, you need to specify the commit SHA of HF dataset.
        // You can find them in https://huggingface.co/datasets/<dataset-name>/commits/main
        git_commit_sha: '070042b...............', // Mandatory
    },
    // Option 2 (delete if not needed): Use a publicly accessible URI
    data_source: {
        type: 'manual',
        // We currently support .jsonl format. Look at the [FAQ](#faq) for an example
        test: 'https://somewebsite.com/path/to/test.jsonl',
        validation: 'https://somewebsite.com/path/to/validation.jsonl', // Optional
        train: 'https://somewebsite.com/path/to/train.jsonl', // Optional
    },
    
    // Providing a test set is mandatory. Depending on the generalization protocol
    // the task is implementing, you can also provide a train + validation set.
    // (e.g. first finetuining on train + validation and then evaluating on test)
    has_validation_set: true, // Default false
    has_train_set: true, // Default false
    
    // We currently support three task types: 
    // 'free_form', 'multi_choice', and 'sequence_labeling'
    // The task type selected here must match the choices in other fields 
    // (e.g. "free_form_output_regex", or "field_mapping")
    task_type: 'multi_choice',
    
    // If the task is a free form generation, we use the following
    // regex to extract the answer.
    free_form_output_regex: '[^\.\?\!\;\n]+', // Optional

    // The task has to provide two fields per example: input and target. The field requirements
    // are different based on the type of task defined above.
    // Free-form tasks:
    // - Input: string
    // - Target: string
    // Sequence-labeling tasks:
    // - Input: list of strings (sequence tokens)
    // - Target: list of labels (matching the size of the input)
    // Multiple-choice tasks:
    // - Input: string
    // - Target: index of choice (target)
    // - Target Options: list of options (string) to choose from

    // Provide a mapping from the fields in the data source to the fields that the task ('input',
    // 'target') expects.
    field_mapping: {
        input: 'hf_ds_field_1',
        target: 'hf_ds_field_2',
    },

    // If you want to re-split the original dataset, you can provide a
    // `split.jsonnet` file that contains the split information. The file should
    // contain a dictionary with three keys: 'train', 'validation', and 'test'. Each key
    // should contain a list of indices that correspond to the examples in the original
    // dataset that should be included in the split. 
    // (See an example of [split.jsonnet](#splitjsonnet) below)
    split_file: 'split.jsonnet',  // Optional.
    

    // Provide a list of evaluation metrics for the task. 
    // At least one evaluation metric has to be provided.
    // Use this field to list HuggingFace evaluation metrics. 
    // If you want to use a custom evaluation metric, you can implement it in the
    // task's [Python class](#taskpy).
    evaluation_metrics: [
        {
            hf_id: 'accuracy',
        },
        {
            hf_id: 'f1', 
        },
    ],

    // Provide a "recipe" for how to prepare the model for the task. 
    // Currently we support "finetuning" and "prompt_based_testing".
    // You need to provide at least one of the two options, but can provide both to cover more 
    // model classes.
    preparation_strategies: {
        // Finetuning the model on the task's train-set and then evaluating
        // on the task's test-set. This is suitable for models such as RoBERTa, BERT, etc.,
        // but can be used for LLMs as well.
        finetuning: {
            objective: 'maximum_likelihood',
            // ... other model-agnostic finetuing options ...
        },

        // Preparing the model to perform the task by configuring its prompt.
        // This recipe is suitable for generative LMs such as GPT-3, OPT, T5, etc.
        // To provide a custom prompt preparation use the task's 
        // [Python class](#custom-metricevaluation-metric).
        prompt_based_testing: {
            prompt_builder: {
                // Currently, we follow BIG-bench options for prompt construction: 
                // https://github.com/google/BIG-bench/blob/main/docs/doc.md#optional-fields
                instruction: 'Add two numbers together',
                input_prefix: 'Q: ',
                output_prefix: 'A: ',
                choice_prefix: '\n  choice: ',
                append_choices_to_input: true,
                few_shot_example_separator: '\n',
                stop_string: '\n\n',
            }
        },
    },
}
```

#### `task.py`
```python
from typing import Any, Dict, List

import datasets

from genbench.tasks import Task


@Task.register("my_awesome_task")
class MyAwesomeTask(Task):
    """Python implementation of the MyAwesomeTask task.

    By default, the task's config.jsonnet should support most of the use-cases, thus
    you don't have to do anything here. However, if the task requires
    some custom logic, you can override any / all of the following
    methods:
    """

    def format_example(self, example: Dict[str, Any]) -> Dict[str, Any]:
        """Perform preprocessing/formatting on an example-level.
        
        By default, this method does nothing more than mapping original data source
        fields to the expected fields.
        
        `example` directly comes from the data source (e.g. downloaded HF dataset),
        and it may contain fields such as `question` or `answer`. This method should 
        prepare the example used in the task. i.e. should create fields `input`, 
        `target`, `target_scores`, or `target_labels` depending on the task type.
        
        Args:
            example: A dictionary containing key-value pairs for an example from the source dataset.
                     
                     
        Returns:
            A dictionary containing key-value pairs for the preprocessed/formatted example.
            The dictionary should contain keys `input`, `target`, `target_scores`, or `target_label`
            depending on the task type.
        """
        ...

    def evaluate_predictions(
        self,
        *,
        predictions: List[Dict[str, Any]] = None,
        gold: datasets.Dataset = None,
    ) -> Dict[str, float]:
        """Evaluate the predictions of the model against the gold data.
        
        By default, this method applies the metric specified in the task's
        config.jsonnet.
        
        Args:
            predictions: A list of dictionaries, where each dictionary contains the predicted
                         values for an example. The keys are strings and the values can be any type.
            gold: A HuggingFace `datasets.Dataset` object containing the ground truth data for the task.
            
        Returns:
            A dictionary containing key-value pairs for the evaluation metric(s) computed on the predicted
            values. The keys are strings representing the name of the evaluation metric and the values are
            floating-point numbers.
        """
        ...

    def get_dataset_raw(self) -> Dict[str, datasets.Dataset]:
        """Get the raw dataset.
        
        By default, this method loads the dataset specified in the task's
        config.jsonnet, and re-split it based on split.json if it exists.
        If the task creator wishes to mix and match data points, they can
        override this method.
        
        Args:
            None
            
        Returns:
            A dictionary containing key-value pairs for the raw datasets. 
            The keys are strings representing the name of the dataset split 
            (e.g., "train", "validation", "test") and the values are
            HuggingFace `datasets.Dataset` objects containing the raw data for the corresponding split.
        """
        ...
```

#### `split.jsonnet`
If you are resplitting the original data source, create a `split.jsonnet` file inside the task's directory, and use it to re-distribute examples. The format is as follows:
```jsonnet
{
    train: ["train:10", "validation:0", "test:21", "test:21", "train:110", ...],
    validation: ["train:19", "test:49", "validation:32", "test:21", ...],
    test: ["validation:32", "train:394", "test:94", "test:485", "validation:192", "test:405", ...], 
}
```

#### `doc.md`
A brief explaination of the task, its motivation and a description of the submssion data. Minimally, this should include: what generalisation property(ies) the task is testing for (GenBench taxonomy values); what assumptions are made about the training data; the size of the dataset; baseline scores. If it already contains this information, feel free to copy the abstract of the accompanying paper.

### Manual data sources
#### File format
Currently, we only support `.jsonl` (jsonline), where each example is a json object presented in a single line.
Here is an example:
```jsonl
{"input": "300 + 80", "target": "380"}
{"input": "301 + 82", "target": "383"}
```

#### File access
The files should be accessible via a single URI per split file (train, test, validation).

#### License
The dataset should licensed under: TBD

## Most Common Use Cases (Examples)
### Train-Test (finetuning)
[CoLA](https://nyu-mll.github.io/CoLA/) resplitting:
`config.jsonnet`
```jsonnet
{
    name: 'CoLA Length Generalization',
    description: 'A re-split of the CoLA dataset to put shorter sentences in the train set and longer ones in the test set.',

    keywords: [
        'sample_task',
        'length_generalization',
    ],

    authors: [
        'GenBench team',
    ],

    data_source: {
        type: 'hf',
        hf_id: ['glue', 'cola'],
        git_commit_sha: '070042b9c631247b37d596ad3cc1a21c896006fd'
    },
    
    has_validation_set: true,
    has_train_set: true,
    
    task_type: 'multi_choice',
    
    field_mapping: {
        input: 'sentence',
        target: 'label',
    },

    split_file: 'split.jsonnet', 
    
    evaluation_metrics: [
        {
            hf_id: 'matthews_correlation',
        },
    ],
    
    preparation_strategies: {
        finetuning: {
            objective: 'maximum_likelihood',
        },
    },
}
```
`split.jsonnet`
```jsonnet
{
    train: ["train:88", "test:11", "test:12", "test:13",...],
    validation: ["validation:14", "train:3", ],
    test: ["train:90", "validation:38", ...], 
}
```

### Prompt-based testing
This is an example of a configuration for a prompt-based task (free-form generation). The task tests a model's capability for adding two numbers; it does not have a validation or training set and evaluates the model using HuggingFace's exact match metric.

```jsonnet
{
    name: 'Sample LLM  json task',
    description: 'Sample LLM task with dummy data that works with only json, for illustration purposes',

    keywords: [
        'sample_task',
    ],

    authors: [
        'GenBench team',
    ],

    data_source: {
        type: 'manual',
        test: 'https://github.com/GenBench/genbench_cbt/dummy_data/LLM_test.jsonl',
    },

    has_validation_set: false,
    has_train_set: false,

    task_type: 'free_form',

    evaluation_metrics: [
        {
            type: 'hf',
            path: ['EM'],
        }
    ],

    preparation_strategies: {
        prompt_based_testing: {
            instruction: 'Add two numbers together',
            input_prefix: 'Q: ',
            output_prefix: 'A: ',
        },
    },
}
```

### Custom `task.py` examples
As a reminder, the following table is the list of methods that can be overriden when defining a task through the Python code. See the [`task.py`](#taskpy) section for more details.

| Method | Description | Inputs | Outputs |
| --- | --- | --- | --- |
| `format_example` | Perform preprocessing/formatting on an example-level | dictionary containing key-value pairs for an example from the source dataset | dictionary containing key-value pairs for the preprocessed/formatted example |
| `evaluate_predictions` | Evaluate the predictions of the model against the gold data | `predictions`: list of dictionaries, where each dictionary contains the predicted values for an example, `gold`: HuggingFace `datasets.Dataset` object containing the ground truth data for the task. | dictionary containing key-value pairs for the evaluation metric(s) computed on the predicted values |
| `get_dataset_raw` | Get the raw dataset | None | dictionary containing key-value pairs for the raw datasets |


#### Custom Metric/Evaluation Metric
Custom logic for evaluating the predictions of a model can be implemented
in the `evaluate_predictions` method in the task's Python class.
`predictions` is a list of dictionaries, where each dictionary contains model predictions.
In this example, we compute the exact match accuracy between the predicted target and the gold target.
```python
@Task.register("my_awesome_qa_task")
class MyAwesomeQATask(Task):
    """Python implementation of the MyAwesomeQATask task.
    A free-form answer generation given a context and a question.
    """

    def evaluate_predictions(
        self,
        *,
        predictions: List[Dict[str, Any]],
        gold: datasets.Dataset,
    ) -> Dict[str, float]:
        """Evaluate the predictions of the model against the gold data.
        Using exact match accuracy as the evaluation metric.

        Args:
            predictions: A list of dictionaries, where each dictionary contains the predicted
                         values for an example. The keys are strings and the values can be any type.
            gold: A HuggingFace `datasets.Dataset` object containing the ground truth data for the task.

        Returns:
            A dictionary containing key-value pairs for the evaluation metric(s) computed on the predicted
            values. The keys are strings representing the name of the evaluation metric and the values are
            floating-point numbers.
        """

        # Compute the exact match accuracy.
        em = 0
        for pred, gold in zip(predictions, gold):
            if pred["target"] == gold["target"]:
                em += 1

        em /= len(predictions)

        # Return the evaluation metrics.
        return {"exact_match": em}
```
Note that when custom logic is implemented in the `evaluate_predictions` method,
the `evaluation_metrics` in the task's config file will be completely ignored.

#### Custom Example Formatting/Pre-processing
Custom logic for pre-processing/formatting examples can be implemented 
in the `format_example` method in the task's Python class. 
In this example, we combine the context and question to create the input 
and directly use the answer as the target.
```python  
from typing import Any, Dict

from genbench.tasks import Task
from genbench.utils import tokenization_utils


@Task.register("my_awesome_qa_task")
class MyAwesomeQATask(Task):
    """Python implementation of the MyAwesomeQATask task.
    A free-form answer generation given a context and a question.
    """

    def format_example(self, example: Dict[str, Any]) -> Dict[str, Any]:
        """Perform preprocessing/formatting on an example-level.
        Map the `context`, `question` to input and `answer` to target.

        Args:
            example: A dictionary containing key-value pairs for an example from the source dataset.


        Returns:
            A dictionary containing key-value pairs for the preprocessed/formatted example.
        """
        input = f"{example['context']} {tokenization_utils.SEP_TOEKN} {example['question']}"
        target = example["answer"]
        return {
            "input": input, 
            "target": target
        }
```
Note that when custom logic is implemented in the `format_example` method,
the `field_mapping` in the task's config file will be completely ignored.

#### Custom Dataset Preparation Loop
The `self.get_dataset_raw()` method is responsible for creating the raw dataset.  
Overriding this method allows you to customize the entire dataset preparation loop.
You can use any method you want and do all sorts of mix and match to create the dataset.
In the example below, we show how to combine every three data instances together, but you can do anything you want.
```python
from typing import Any, Dict

import datasets

from genbench.tasks import Task

@Task.register("my_magical_task")
class MyMagicalTask(Task):
    """Python implementation of the MyAwesomeTask task."""

    def get_dataset_raw(self) -> Dict[str, datasets.Dataset]:
        """Create the dataset by mixing every three data instance together.

        Args:
            None

        Returns:
            A dictionary containing key-value pairs for the raw datasets.
            The keys are strings representing the name of the dataset split
            (e.g., "train", "validation", "test") and the values are
            HuggingFace `datasets.Dataset` objects containing the raw data for the corresponding split.
        """
        # Load the raw datasets
        raw_datasets: Dict[str, datasets.Dataset] = self._load_data_source()

        # Mix every three data instances together per each split
        output: Dict[str, datasets.Dataset] = {}
        for split, dataset in raw_datasets.items():
            # Combine every three data instances together
            dataset = dataset.map(self._magic_combo, batched=True, batch_size=3)

            # Maybe do additional processing/formatting here
            dataset = dataset.map(self.format_example)

            output[split] = dataset

        return output

    def _magic_combo(self, examples: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
        """Combine every three data instances together.

        Args:
            examples: A dictionary containing key-value pairs for the data instances.
                The keys are strings representing the name of the data instance
                (e.g., "input", "target") and the values are lists containing
                the data instance values.

        Returns:
            A dictionary containing key-value pairs for the combined data instances.
            The keys are strings representing the name of the data instance
            (e.g., "input", "target") and the values are lists containing
            the combined data instance values.
        """
        
        single_example: Dict[str, Any] = {}

        # Perform some cool mixing magic here
        # ...

        # HuggingFace datasets.Dataset.map() expects
        # a dictionary of lists as output
        output = {k: [v] for k, v in single_example.items()}

        return output
```
