from genbench.utils.tasks import get_task_dir


def test_contains_all_files(task_id):
    """Test case to verify if all the required files are present in the task directory"""

    # List of files that should exist in the task directory
    required_files = [
        "__init__.py",
        "config.jsonnet",
        "task.py",
        "doc.md",
    ]

    # Get the task directory based on the task_id
    task_dir = get_task_dir(task_id)

    # Check if each required file exists in the task directory
    for file in required_files:
        assert (task_dir / file).exists()


def test_split_file_has_task_provided_sets(task_id):
    ...


def test_task_config_matches_provided_sets(task_id):
    ...


def test_task_examples_match_task_type(task_id):
    ...


def test_no_duplicate_examples(task_id):
    ...


def test_no_iterable_dataset(task_id):
    ...


def test_if_in_context_learning_has_target_options(task_id):
    ...


def test_prompt_builder_is_default(task_id):
    ...
