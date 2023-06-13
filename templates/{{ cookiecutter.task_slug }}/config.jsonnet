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
        '{{ cookiecutter.task_author }}',
    ],

    data_source: {
        type: 'manual',
        test: 'https://github.com/GenBench/genbench_cbt/dummy_data/LLM_test.jsonl',
    },

    has_validation_set: false,
    has_train_set: false,

    task_type: 'free_form',

    evaluation_metrics: [
        {
            type: 'hf',
            path: ['EM'],
        }
    ],

    prepation_strategies: {
        prompt_based_testing: {
            instruction: 'Add two numbers together',
            input_prefix: 'Q: ',
            output_prefix: 'A: ',
        },
    },
}