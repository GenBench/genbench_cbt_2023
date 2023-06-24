from typing import List

import click

from genbench.utils.file import get_repo_dir
from genbench.utils.logging import get_logger
from genbench.utils.tasks import (
    get_all_tasks_ids,
    is_valid_task_id,
    generate_task_from_template,
    get_tasks_dir,
)

logger = get_logger(__name__)


def is_cookiecutter_installed() -> bool:
    """Check if cookiecutter is installed."""
    try:
        from cookiecutter.main import cookiecutter  # noqa: F401

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

    > genbench-cli create-task --name "The addition task" --id "addition" --s "subtask_1" --s "subtask_2"
    """
    # Check if cookiecutter is installed
    if not is_cookiecutter_installed():
        raise click.UsageError(
            "Cookiecutter is not installed. Please use `pip install genbench[dev]` to install it."
        )

    # Make sure `name` only contains ascii characters
    if not all(ord(c) < 128 for c in name):
        raise click.UsageError(
            "Task name can only contain ascii characters. "
            "Please use only alphanumeric characters."
        )

    # If `id_` is not provided, use `name` to create `id_`
    if id_ is None:
        id_ = "_".join(name.lower().split())

    # Make sure `id` only contains alphanumeric characters and underscores and lower case
    if not is_valid_task_id(id_):
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

    task_authors = click.prompt("Task authors (e.g John Doe). Split with ','", type=str)

    if len(subtask_ids) == 0:
        task_class_name = "".join([w.capitalize() for w in id_.split("_")])
        task_class_name = f"{task_class_name}Task"

        click.echo(f"Creating task...")
        click.echo(f"Task name: {name}")
        click.echo(f"Task id: {id_}")
        click.echo(f"Task class name: {task_class_name}")

        generate_task_from_template(
            name=name,
            task_id=id_,
            task_class_name=task_class_name,
            task_authors=task_authors,
        )

        click.echo(f"\n\nTask created successfully.")
        click.echo(f"View the task at {get_repo_dir() / 'genbench' / 'tasks' / id_}")
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

        click.echo(f"Creating task dict...")
        click.echo(f"TaskDict name: {name}")
        click.echo(f"Task id: {id_}")
        click.echo(f"TaskDict class name: {task_dict_class_name}\n")

        from cookiecutter.main import cookiecutter

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
        click.echo(f"Creating subtasks...\n\n")
        for subtask_id in subtask_ids:
            subtask_name = f"{name} ({subtask_id})"

            # We use the following naming convention for subtasks:
            # TaskDictClassnameSubtaskClassname
            subtask_class_name = "".join(
                [w.capitalize() for w in subtask_id.split("_")]
            )
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

            click.echo(f"Done!")
            click.echo(
                f"View the subtask at {get_repo_dir() / 'genbench' / 'tasks' / id_ / subtask_id}\n"
            )

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
