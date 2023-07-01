import sys
from pathlib import Path
from typing import List

import click
import pytest

from genbench.utils.file import get_repo_dir
from genbench.utils.logging import get_logger
from genbench.utils.tasks import (
    generate_task_from_template,
    get_all_tasks_and_subtasks_ids,
    get_all_tasks_ids,
    get_task_dict_subtasks,
    get_task_dir,
    get_tasks_dir,
    is_task_dict,
    is_valid_task_id,
)


logger = get_logger(__name__)


def is_cookiecutter_installed() -> bool:
    """Check if cookiecutter is installed."""
    try:
        from cookiecutter.main import cookiecutter  # noqa: F401

        return True
    except ImportError:
        return False


def is_git_python_installed() -> bool:
    """Check if git-python is installed."""
    try:
        import git  # noqa: F401

        return True
    except ImportError:
        return False


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    """genbench-cli is a command line interface for GenBench collaborative benchmarking task.
    It provides a set of commands to create tasks, run tests, and prepare submissions.
    """
    ctx.ensure_object(dict)


@cli.command()
@click.option(
    "-n",
    "--name",
    type=str,
    required=True,
    help="Name of the task. e.g. 'The addition task'",
)
@click.option(
    "-i",
    "--id",
    "id_",  # `id` is a reserved keyword in Python
    type=str,
    metavar="ID",
    help=(
        "Unique id of the task. e.g. 'addition'. "
        "No spaces allowed. Use only alphanumeric characters (lower case) and underscores"
    ),
)
@click.option(
    "-s",
    "--subtask_ids",
    type=str,
    multiple=True,
    metavar="SUBTASK_ID",
    help=(
        "Unique id of the subtask. e.g. '-s subtask_1 -s subtask_2'. "
        "No spaces allowed. Use only alphanumeric characters (lower case) and underscores."
        ""
    ),
)
@click.pass_context
def create_task(ctx: click.Context, name: str, id_: str, subtask_ids: List[str]):
    """
    Create a new task with the provided name, id, and optional subtask ids.

    Usage Examples:

    1. Basic usage:

    > genbench-cli create-task --name "The addition task" --id "addition"

    2. Creating a task with subtasks:

    > genbench-cli create-task --name "The addition task" --id "addition" -s "subtask_1" -s "subtask_2"
    """
    # Check for extra dependencies
    if not is_cookiecutter_installed():
        raise click.UsageError(
            "Cookiecutter is not installed. Please use `pip install -e genbench[dev]` to install it."
        )
    if not is_git_python_installed():
        raise click.UsageError("GitPython is not installed. Please use `pip install -e genbench[dev]` to install it.")

    # Make sure we are not on the main branch
    import git

    repo = git.Repo(get_repo_dir())
    current_branch = repo.active_branch.name
    if current_branch == "main":
        raise click.UsageError("Please create a new branch before creating a task.")

    # Make sure `name` only contains ascii characters
    if not all(ord(c) < 128 for c in name):
        raise click.UsageError("Task name can only contain ascii characters. Please use only alphanumeric characters.")

    # If `id_` is not provided, use `name` to create `id_`
    if id_ is None:
        id_ = "_".join(name.lower().split())

    # Make sure `id` only contains alphanumeric characters and underscores and lower case
    if ":" in id_:
        raise click.UsageError(
            "You cannot use ':' in task id. Please use only alphanumeric characters (lower case) and underscores."
        )

    if not is_valid_task_id(id_):
        raise click.UsageError(
            "Task id can only contain alphanumeric characters and underscores. "
            "Please use only alphanumeric characters (lower case) and underscores."
        )

    all_tasks_ids = get_all_tasks_ids()
    if id_ in all_tasks_ids:
        raise click.UsageError(
            f"Task with id '{id_}' already exists. Please either specify a different id or use a different name."
        )

    task_authors = click.prompt("Task authors (e.g John Doe). Split with ','", type=str)

    if len(subtask_ids) == 0:
        task_class_name = "".join([w.capitalize() for w in id_.split("_")])
        task_class_name = f"{task_class_name}Task"

        click.echo("Creating task...")
        click.echo(f"Task name: {name}")
        click.echo(f"Task id: {id_}")
        click.echo(f"Task class name: {task_class_name}")

        generate_task_from_template(
            name=name,
            task_id=id_,
            task_class_name=task_class_name,
            task_authors=task_authors,
        )

        click.echo("\n\nTask created successfully.")
        click.echo(f"View the task at {get_repo_dir() / 'src' / 'genbench' / 'tasks' / id_}")
    else:
        # Make sure subtask ids are valid
        for subtask_id in subtask_ids:
            if not is_valid_task_id(subtask_id):
                raise click.UsageError(
                    f"Subtask id '{subtask_id}' is not valid. "
                    "Please use only alphanumeric characters (lower case) and underscores."
                )

        # First create the task dict
        from cookiecutter.main import cookiecutter

        task_dict_class_name = "".join([w.capitalize() for w in id_.split("_")])

        click.echo("Creating task dict...")
        click.echo(f"TaskDict name: {name}")
        click.echo(f"Task id: {id_}")
        click.echo(f"TaskDict class name: {task_dict_class_name}\n")

        cookiecutter(
            str(get_repo_dir() / "templates" / "task_with_subtasks"),
            extra_context={
                "task_name": name,
                "task_id": id_,
                "task_dict_class_name": task_dict_class_name,
                "task_authors": task_authors,
                "subtasks": ",".join(subtask_ids),
            },
            output_dir=str(get_tasks_dir()),
            overwrite_if_exists=True,
            no_input=True,
        )

        # Then create the subtasks
        click.echo("Creating subtasks...\n\n")
        for subtask_id in subtask_ids:
            subtask_name = f"{name} ({subtask_id})"

            # We use the following naming convention for subtasks:
            # TaskDictClassnameSubtaskClassname
            subtask_class_name = "".join([w.capitalize() for w in subtask_id.split("_")])
            subtask_class_name = f"{task_dict_class_name}{subtask_class_name}"

            # Subtasks are created in a subfolder in the task_dict folder
            output_dir = get_tasks_dir() / id_

            click.echo(f"Subtask name: {subtask_name}")
            click.echo(f"Subtask id: {id_}:{subtask_id}")
            click.echo(f"Subtask class name: {subtask_class_name}")

            generate_task_from_template(
                name=subtask_name,
                task_id=subtask_id,
                task_class_name=subtask_class_name,
                task_authors=task_authors,
                output_dir=output_dir,
            )

            click.echo("Done!")
            click.echo(f"View the subtask at {get_repo_dir() / 'src' / 'genbench' / 'tasks' / id_ / subtask_id}\n")

    click.echo(f"Instruction to fill and submit the task at https://github.com/GenBench/genbench_cbt")


@cli.command()
@click.option(
    "-i",
    "--id",
    "id_",  # `id` is a reserved keyword in Python
    type=str,
    required=True,
    metavar="ID",
    help="Id of the task to run tests for. e.g. 'addition'.",
)
@click.option(
    "--tests-dir",
    "tests_dir",
    type=click.Path(exists=True),
    metavar="DIR",
    help="Path to the directory containing the tests. Defaults to 'tests'.",
    default=None,
)
@click.pass_context
def test_task(ctx: click.Context, id_: str, tests_dir: str = None):
    """Run tests for a task."""

    if id_ is None:
        raise click.UsageError("Please specify the task id. e.g. 'genbench-cli test-task --id addition'")
    # Make sure task exists
    all_tasks_ids = get_all_tasks_and_subtasks_ids()
    if id_ not in all_tasks_ids:
        raise click.UsageError(f"Task with id '{id_}' does not exist. Please specify a valid task id.")

    if tests_dir is None:
        task_test_path = get_repo_dir() / "tests" / "test_task.py"
    else:
        click.echo(f"Using tests directory: {tests_dir}")
        task_test_path = Path(tests_dir) / "test_task.py"

    if ":" not in id_ and is_task_dict(get_task_dir(id_)):
        # If task is a task dict, we need to run tests for each subtask
        subtasks = get_task_dict_subtasks(get_task_dir(id_))
        for subtask_id in subtasks:
            ctx.invoke(test_task, id_=f"{id_}:{subtask_id}", tests_dir=tests_dir)
    else:
        exit_code = pytest.main(["-xrpP", task_test_path, f"--task-id={id_}"])
        if exit_code != 0:
            sys.exit(exit_code)


@cli.command()
@click.option(
    "-i",
    "--id",
    "id_",  # `id` is a reserved keyword in Python
    type=str,
    required=True,
    metavar="ID",
    help="Id of the task. e.g. 'addition'.",
)
@click.option(
    "--check-uncommitted-changes/--no-check-uncommitted-changes",
    default=True,
    help="Check for uncommitted changes before submitting the task. Defaults to True.",
)
@click.option(
    "--check-unpushed-changes/--no-check-unpushed-changes",
    default=True,
    help="Check for unpushed changes before submitting the task. Defaults to True.",
)
@click.pass_context
def submit_task(ctx: click.Context, id_: str, check_uncommitted_changes: bool, check_unpushed_changes: bool):
    """Create a pull request for a task."""
    if ":" in id_:
        raise click.UsageError(
            f"Please specify a task_dict id. e.g. 'genbench-cli submit-task --id {id_.split(':')[0]}'"
        )

    # Make sure task exists
    all_tasks_ids = get_all_tasks_and_subtasks_ids()
    if id_ not in all_tasks_ids:
        raise click.UsageError(f"Task with id '{id_}' does not exist. Please specify a valid task id.")

    if not is_git_python_installed():
        raise click.UsageError("Please install gitpython to use this command. e.g. 'pip install -e genbench[dev]'")

    import git

    repo = git.Repo(get_repo_dir())
    current_branch = repo.active_branch.name

    # if current_branch == "main":
    #     raise click.UsageError("Please submit your task from a branch other than 'main'.")

    # Make sure there are no uncommitted changes
    if check_uncommitted_changes and repo.is_dirty():
        raise click.UsageError(
            "Please commit your changes before submitting a task. "
            "Use --no-check-uncommitted-changes to ignore this check."
        )

    # Make sure there are no unpushed commits
    unpushed_commits = list(repo.iter_commits(f"{current_branch}@{{u}}..{current_branch}"))
    if check_unpushed_changes and unpushed_commits:
        raise click.UsageError(
            "Please push your commits before submitting a task. Use --no-check-unpushed-changes to ignore this check."
        )

    # Extract the username and repo name from the remote url
    remote_url = repo.config_reader().get_value('remote "origin"', "url")
    assert "github.com" in remote_url, "Only GitHub is supported for now."

    username, repo_name = remote_url.split("github.com/")[1].split("/")[:2]
    repo_name = repo_name.replace(".git", "")
    click.echo(f"Fork Repo: {username}/{repo_name}")

    # Construct the PR URL
    from genbench import load_config

    task_config = load_config(id_)
    from genbench import TaskConfig
    if isinstance(task_config, TaskConfig):
        task_name = task_config.name
    else:
        task_name = task_config["name"]
    title = f"[Task Submission] {task_name} (`{id_}`)"
    "quick_pull=1&template=task_submission.md&labels=task-submission&title=[Task Submission] Sample Task 2"
    pr_url = f"https://github.com/GenBench/genbench_cbt/compare/main...{username}:{repo_name}:{current_branch}"
    query_params = {
        "quick_pull": 1,
        "template": "task_submission.md",
        "labels": "task-submission",
        "title": title,
    }

    from urllib.parse import urlencode

    pr_url += "?" + urlencode(query_params)

    click.echo("\n" + "-" * 80)
    click.echo("Click the link below to create a pull request for the task:")
    click.echo(pr_url)
    click.echo("\nPlease do not change the title of the pull request.")
    click.echo("-" * 80 + "\n")
