{
    name: '{{ cookiecutter.task_name }}',

    // @TODO: Add a description of the task
    description: '{{ cookiecutter.task_name }} aims to measure ...',

    // @TODO: Add a list of keywords that describe the task
    keywords: [
        'keyword1',
        'keyword2',
    ],

    authors: [
        {% for author in cookiecutter.task_authors.split(",") %}'{{ author }}',
        {% endfor %}
    ],

    subtasks_order: [
        {% for subtask in cookiecutter.subtasks.split(",") %}'{{ subtask }}',
        {% endfor %}
    ],
}