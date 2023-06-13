from pathlib import Path
from typing import List

import click
from cookiecutter.main import cookiecutter

import genbench.tasks
from genbench.utils.file import get_repo_dir
from genbench.utils.logging import get_logger
from genbench.utils.tasks import get_all_tasks_ids

logger = get_logger(__name__)


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
@click.pass_context
def create_task(ctx: click.Context, name: str, id_: str):
    """Create a new task."""
    # Make sure `name` only contains ascii characters
    if not all(ord(c) < 128 for c in name):
        raise click.UsageError(
            "Task name can only contain ascii characters. "
            "Please use only alphanumeric characters."
        )

    # If `id_` is not provided, use `name` to create `id_`
    if id_ is None:
        id_ = name.lower().replace(" ", "_")

    # Make sure `id` only contains alphanumeric characters and underscores and lower case
    if not all(
        (c.isalnum() and ord(c) < 128 and c.lower() == c) or c == "_" for c in id_
    ):
        raise click.UsageError(
            "Task id can only contain alphanumeric characters and underscores. "
            "Please use only alphanumeric characters (lower case) and underscores."
        )

    all_tasks_ids = get_all_tasks_ids()
    if id_ in all_tasks_ids:
        raise click.UsageError(
            f"Task with id '{id_}' already exists. "
            "Please either specify a different id or use a different name."
        )

    task_class_name = "".join([w.capitalize() for w in id_.split("_")])

    task_author = click.prompt("Task author (e.g John Doe)", type=str)

    click.echo(f"Creating task...")
    click.echo(f"Task name: {name}")
    click.echo(f"Task id: {id_}")
    click.echo(f"Task class name: {task_class_name}")

    # Create task
    cookiecutter(
        str(get_repo_dir() / "templates"),
        extra_context={
            "task_name": name,
            "task_id": id_,
            "task_class_name": task_class_name,
            "task_author": task_author,
        },
        output_dir=str(Path(genbench.tasks.__file__).parent),
        overwrite_if_exists=True,
        no_input=True,
    )

    click.echo(f"\n\nTask created successfully.")
    click.echo(f"View the task at {get_repo_dir() / 'genbench' / 'tasks' / id_}")
    click.echo(
        f"Instruction to fill and submit the task at {get_repo_dir() / 'README.md'}"
    )


@cli.command()
@click.option(
    "-i",
    "--id",
    "id_",  # `id` is a reserved keyword in Python
    type=str,
    metavar="ID",
    help="Id of the task to run tests for. e.g. 'addition'.",
)
@click.pass_context
def test_task(ctx: click.Context, id_: str):
    """Run tests for a task."""

    import pytest

    if id_ is None:
        raise click.UsageError(
            "Please specify the task id. e.g. 'genbench-cli test-task --id addition'"
        )
    # Make sure task exists
    all_tasks_ids = get_all_tasks_ids()
    if id_ not in all_tasks_ids:
        raise click.UsageError(
            f"Task with id '{id_}' does not exist. Please specify a valid task id."
        )

    task_test_path = get_repo_dir() / "tests" / "test_task.py"

    return pytest.main(["-xrpP", task_test_path, f"--task-id={id_}"])
