from genbench.utils.tasks import get_task_dir


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
