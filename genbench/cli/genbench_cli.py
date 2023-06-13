from pathlib import Path

import click

from cookiecutter.main import cookiecutter

import genbench.tasks
from genbench.utils.file import get_repo_dir
from genbench.utils.logging import get_logger
from genbench.utils.tasks import get_all_tasks_slugs

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
    "-s",
    "--slug",
    type=str,
    help=(
        "Unique slug (id) of the task. e.g. 'addition'. "
        "No spaces allowed. Use only alphanumeric characters and underscores"
    ),
)
@click.pass_context
def create_task(ctx: click.Context, name: str, slug: str):
    """Create a new task."""
    # Make sure `name` only contains ascii characters
    if not all(ord(c) < 128 for c in name):
        raise click.UsageError(
            "Task name can only contain ascii characters. "
            "Please use only alphanumeric characters."
        )

    # If `slug` is not provided, use `name` to create `slug`
    if slug is None:
        slug = name.lower().replace(" ", "_")

    # Make sure `slug` only contains alphanumeric characters and underscores
    if not all((c.isalnum() and ord(c) < 128) or c == "_" for c in slug):
        raise click.UsageError(
            "Task slug can only contain alphanumeric characters and underscores. "
            "Please use only alphanumeric characters and underscores."
        )

    all_tasks_slugs = get_all_tasks_slugs()
    if slug in all_tasks_slugs:
        raise click.UsageError(
            f"Task with slug '{slug}' already exists. "
            "Please either specify a different slug or use a different name."
        )

    task_class_name = "".join([w.capitalize() for w in slug.split("_")])

    task_author = click.prompt("Task author (e.g John Doe)", type=str)

    click.echo(f"Creating task...")
    click.echo(f"Task name: {name}")
    click.echo(f"Task slug: {slug}")
    click.echo(f"Task class name: {task_class_name}")

    # Create task
    cookiecutter(
        str(get_repo_dir() / "templates"),
        extra_context={
            "task_name": name,
            "task_slug": slug,
            "task_class_name": task_class_name,
            "task_author": task_author,
        },
        output_dir=str(Path(genbench.tasks.__file__).parent),
        overwrite_if_exists=True,
        no_input=True,
    )

    click.echo(f"\n\nTask created successfully.")
    click.echo(f"View the task at {get_repo_dir() / 'genbench' / 'tasks' / slug}")
    click.echo(
        f"Instruction to fill and submit the task at {get_repo_dir() / 'README.md'}"
    )
