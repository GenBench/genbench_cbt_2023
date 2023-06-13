from genbench.tasks import Task


@Task.register("{{ cookiecutter.task_slug }}")
class {{ cookiecutter.task_class_name }}(Task):
      pass