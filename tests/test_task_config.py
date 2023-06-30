import pytest

from genbench import TaskConfig


TASK_CONFIG_SKELETON = """\
{{
    name: 'My Awesome Task',
    description: 'Some short description of it',
    keywords: {keywords},
    authors: {authors},
    data_source: {data_source},
    has_validation_set: true,
    has_train_set: true,
    task_type: {task_type},
    free_form_output_regex: '',
    field_mapping: {field_mapping},
    split_file: {split_file},
    evaluation_metrics: {evaluation_metrics},
    preparation_strategies: {preparation_strategies},
}}
"""


@pytest.fixture
def default_jsonnet_config() -> str:
    data_source_config = """{
        type: 'hf',
        hf_id: 'snli',
        git_commit_sha: '070042b...............', // Mandatory
    }"""

    field_mapping = """{
        input: 'hf_ds_field_1',
        target: 'hf_ds_field_2',
    }"""

    evaluation_metrics = """[
        {
            hf_id: 'accuracy',
            git_commit_sha: "758135da6a37ce962b7bc38c6dd5eab672d2b742",
            best_score: 1.0,
        },
    ]"""

    preparation_strategies = """{
        prompt_based_testing: {
            prompt_builder: {
                instruction: 'Add two numbers together',
                input_prefix: 'Q: ',
                output_prefix: 'A: ',
                choices_prefix: '\\n  choice: ',
                append_choices_to_input: true,
                few_shot_example_separator: '\\n',
                stop_string: '\\n\\n',
            }
        }
    }
    """

    return TASK_CONFIG_SKELETON.format(
        keywords="['addition', 'math', 'numbers']",
        authors="['John Doe']",
        data_source=data_source_config,
        task_type="'free_form'",
        field_mapping=field_mapping,
        split_file="'split.json'",
        evaluation_metrics=evaluation_metrics,
        preparation_strategies=preparation_strategies,
    )


def test_from_jsonnet(default_jsonnet_config):
    print(default_jsonnet_config)
    c = TaskConfig.from_jsonnet(jsonnet_str=default_jsonnet_config)
    assert c.name == "My Awesome Task"
    assert c.description == "Some short description of it"
    assert c.keywords == ["addition", "math", "numbers"]
