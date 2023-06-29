import json
from pathlib import Path
from random import Random

import pytest

from genbench import Task
from genbench.api import PreparationStrategy

FREE_FORM_EXAMPLE_INPUT_TEMPLATE = "{input_prefix}{input}{output_prefix}"
FREE_FORM_EXAMPLE_TARGET_TEMPLATE = "{output}"

MULTI_CHOICE_EXAMPLE_INPUT_TEMPLATE = (
    "{input_prefix}{input}{choice_prefix}{choices}{output_prefix}"
)
MULTI_CHOICE_EXAMPLE_TARGET_TEMPLATE = "{target}"

ZERO_SHOT_ICL_TEMPLATE = "{instruction}{example_input}"


def generate_random_string(length: int, rng: Random) -> str:
    """Generate a random string of a given length with spcae characters."""
    import string

    return "".join(rng.choice(string.ascii_letters + " ") for _ in range(length))


def generate_default_config(data_file):
    config = {
        "name": "Free Form Test Task",
        "description": "A test task for free form text.",
        "keywords": ["free form", "text"],
        "authors": ["GenBench team"],
        "data_source": {
            "type": "manual",
            "test": data_file.absolute().as_uri(),
        },
        "has_validation_set": False,
        "has_train_set": False,
        "task_type": "free_form",
        "free_form_output_regex": ".*",
        "evaluation_metrics": [
            {
                "hf_id": "exact_match",
                "git_commit_sha": "758135da6a37ce962b7bc38c6dd5eab672d2b742",
                "best_score": 1.0,
            }
        ],
        "preparation_strategies": {
            "finetuning": {
                "objective": "maximum_likelihood",
            },
            "prompt_based_testing": {
                "prompt_builder": {
                    "instruction_zero_shot": "Add two numbers together\n\n",
                    "instruction_few_shot": "Add two numbers together. Here are some examples: \n\n",
                    "input_prefix": "Q: ",
                    "output_prefix": "\nA: ",
                },
            },
        },
    }
    return config


def generate_addition_task_data(num_examples):
    rng = Random(42)
    data = []
    for _ in range(num_examples):
        a = rng.randint(0, 100)
        b = rng.randint(0, 100)
        input_str = f"{a} + {b}"
        target = str(a + b)
        data.append({"input": input_str, "target": target})
    return data


def generate_multi_choice_task_data(num_examples):
    rng = Random(42)
    data = []
    for _ in range(num_examples):
        input_str = generate_random_string(rng.randint(20, 100), rng)
        target_options = [
            generate_random_string(rng.randint(20, 100), rng) for _ in range(4)
        ]
        target = rng.randint(0, len(target_options) - 1)
        data.append(
            {
                "input": input_str,
                "target": target,
                "target_options": target_options,
            }
        )

    return data


@pytest.fixture
def free_form_task_dir(tmpdir: Path) -> Path:
    # Generate the data
    num_examples = 50
    data = generate_addition_task_data(num_examples)

    # Save the data
    data_file = tmpdir / "data.jsonl"
    with data_file.open("w") as f:
        for example in data:
            f.write(json.dumps(example) + "\n")

    # Generate the config
    config = generate_default_config(Path(data_file))

    config_file = tmpdir / "config.jsonnet"
    with config_file.open("w") as f:
        json.dump(config, f)

    # Add __init__.py
    init_file = Path(tmpdir / "__init__.py")
    init_file.touch()

    # Add the Python class
    task_file = Path(tmpdir / "task.py")
    with task_file.open("w") as f:
        f.write(
            (
                "from genbench import Task\n"
                "\n"
                "\n"
                "class FreeFormTask(Task):\n"
                "\tpass\n"
            )
        )

    return tmpdir


@pytest.fixture
def multi_choice_task_dir(tmpdir: Path) -> Path:
    # Generate the data
    rng = Random(42)
    num_examples = 50
    data = generate_multi_choice_task_data(num_examples)

    # Save the data
    data_file = tmpdir / "data.jsonl"
    with data_file.open("w") as f:
        for example in data:
            f.write(json.dumps(example) + "\n")

    # Generate the config
    config = generate_default_config(Path(data_file))
    config["task_type"] = "multiple_choice"
    config["evaluation_metrics"] = [
        {
            "hf_id": "accuracy",
            "git_commit_sha": "34d6add55811828baef83e0d7c6826e2193f7b6a",
            "best_score": 1.0,
        }
    ]
    config["preparation_strategies"]["prompt_based_testing"]["prompt_builder"][
        "instruction_zero_shot"
    ] = (generate_random_string(rng.randint(20, 100), rng) + "\n\n")
    config["preparation_strategies"]["prompt_based_testing"]["prompt_builder"][
        "instruction_few_shot"
    ] = (generate_random_string(rng.randint(20, 100), rng) + "\n\n")

    config_file = Path(tmpdir / "config.jsonnet")
    with config_file.open("w") as f:
        json.dump(config, f)

    # Add __init__.py
    init_file = Path(tmpdir / "__init__.py")
    init_file.touch()

    # Add the Python class
    task_file = Path(tmpdir / "task.py")
    with task_file.open("w") as f:
        f.write(
            (
                "from genbench import Task\n"
                "\n"
                "\n"
                "class FreeFormTask(Task):\n"
                "\tpass\n"
            )
        )

    return tmpdir


def _load_task(task_dir: Path, task_id) -> Task:
    from genbench import TaskConfig
    import inspect
    import importlib.util

    # Load task config
    config_path = task_dir / "config.jsonnet"
    config = TaskConfig.from_jsonnet(jsonnet_path=config_path)

    spec = importlib.util.spec_from_file_location("task", str(task_dir / "task.py"))

    # creates a new module based on spec
    task_module = importlib.util.module_from_spec(spec)

    # executes the module in its own namespace
    # when a module is imported or reloaded.
    spec.loader.exec_module(task_module)

    # Find task class
    task_class = None
    for name, obj in inspect.getmembers(task_module):
        if inspect.isclass(obj) and issubclass(obj, Task) and obj != Task:
            task_class = obj
            break

    task_obj = task_class(config, task_id)

    return task_obj


@pytest.fixture
def free_form_task(free_form_task_dir) -> Task:
    task_obj = _load_task(Path(free_form_task_dir), "free_form_task")
    task_obj.dataset_format_num_proc = 1
    return task_obj


@pytest.fixture
def multi_choice_task(multi_choice_task_dir) -> Task:
    task_obj = _load_task(Path(multi_choice_task_dir), "multi_choice_task")
    task_obj.dataset_format_num_proc = 1
    return task_obj


def test_free_form_task(free_form_task: Task):
    prompt_builder = (
        free_form_task.config.preparation_strategies.prompt_based_testing.prompt_builder
    )

    # Check all the examples follow the correct format
    # Load the original data
    data_file = Path(free_form_task.config.data_source.test.split("file://")[1])
    with data_file.open("r") as f:
        original_data = [json.loads(line) for line in f]

    ds = free_form_task.get_prepared_datasets(
        preparation_strategy=PreparationStrategy.PROMPT_BASED_TESTING,
        shot_list=[0],
        random_seed=42,
    )[0]
    for orig_exm, exm in zip(original_data, ds):
        formatted_input = FREE_FORM_EXAMPLE_INPUT_TEMPLATE.format(
            input_prefix=prompt_builder.input_prefix,
            input=orig_exm["input"],
            output_prefix=prompt_builder.output_prefix,
        )
        formatted_input = ZERO_SHOT_ICL_TEMPLATE.format(
            instruction=prompt_builder.instruction_zero_shot,
            example_input=formatted_input,
        )
        formatted_target = FREE_FORM_EXAMPLE_TARGET_TEMPLATE.format(
            output=orig_exm["target"]
        )

        assert exm["input"] == formatted_input
        assert exm["target"] == formatted_target

    # Check the evaluation works
    predictions = [
        {"target": f"{exm['target']} {generate_random_string(10, Random(42))}"}
        for exm in original_data[: len(original_data) // 2]
    ]

    predictions += [
        {"target": f"{exm['target']}"}
        for exm in original_data[len(original_data) // 2 :]
    ]

    eval_result = free_form_task.evaluate_predictions(predictions=predictions, gold=ds)
    assert eval_result["hf_exact_match__exact_match"] == 0.5


def test_multi_choice_task(multi_choice_task):
    prompt_builder = (
        multi_choice_task.config.preparation_strategies.prompt_based_testing.prompt_builder
    )

    # Check all the examples follow the correct format
    # Load the original data
    data_file = Path(multi_choice_task.config.data_source.test.split("file://")[1])
    with data_file.open("r") as f:
        original_data = [json.loads(line) for line in f]

    ds = multi_choice_task.get_prepared_datasets(
        preparation_strategy=PreparationStrategy.PROMPT_BASED_TESTING,
        shot_list=[0],
        random_seed=42,
    )[0]
    for orig_exm, exm in zip(original_data, ds):
        formatted_input = MULTI_CHOICE_EXAMPLE_INPUT_TEMPLATE.format(
            input_prefix=prompt_builder.input_prefix,
            input=orig_exm["input"],
            choice_prefix=prompt_builder.choices_prefix,
            choices="".join(
                [
                    f"{prompt_builder.choice_item_prefix}{c}{prompt_builder.choice_item_postfix}"
                    for c in orig_exm["target_options"]
                ]
            ),
            output_prefix=prompt_builder.output_prefix,
        )
        formatted_input = ZERO_SHOT_ICL_TEMPLATE.format(
            instruction=prompt_builder.instruction_zero_shot,
            example_input=formatted_input,
        )
        formatted_target = FREE_FORM_EXAMPLE_TARGET_TEMPLATE.format(
            output=orig_exm["target_options"][orig_exm["target"]]
        )

        assert exm["input"] == formatted_input
        assert exm["target"] == formatted_target

    # Check the evaluation works
    predictions = [
        {
            "target": [
                i for i in range(len(exm["target_options"])) if i != exm["target"]
            ][0]
        }
        for exm in original_data[: len(original_data) // 2]
    ]
    predictions += [
        {"target": f"{exm['target']}"}
        for exm in original_data[len(original_data) // 2 :]
    ]

    eval_result = multi_choice_task.evaluate_predictions(
        predictions=predictions, gold=ds
    )
    assert eval_result["hf_accuracy__accuracy"] == 0.5
