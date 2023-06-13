import pytest


def pytest_addoption(parser):
    parser.addoption("--task-id", action="store")


@pytest.fixture(scope="session")
def task_id(request):
    task_id_value = request.config.option.task_id
    if task_id_value is None:
        pytest.skip()
    return task_id_value
