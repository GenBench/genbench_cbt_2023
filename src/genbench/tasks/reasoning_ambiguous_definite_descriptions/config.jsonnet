{
    name: 'reasoning_ambiguous_definite_descriptions',

    // @TODO: Add a description of the task
    description: 'reasoning_ambiguous_definite_descriptions aims to measure ...',

    // @TODO: Add a list of keywords that describe the task
    keywords: [
        'keyword1',
        'keyword2',
    ],

    authors: [
        'Stefan F. Schouten',
        'Peter Bloem',
        'Ilia Markov',
        'Piek Vossen',
    ],

    data_source: {
        type: 'manual',
        test: 'https://raw.githubusercontent.com/sfschouten/genbench_cbt/reasoning-ambiguous-definite-descriptions/src/genbench/tasks/reasoning_ambiguous_definite_descriptions/benchmark_direct.jsonl',
    },

    has_validation_set: false,
    has_train_set: false,

    task_type: 'multiple_choice',

    field_mapping: {
        input: 'input',
        target: 'label_nr',
    },

    evaluation_metrics: [
        {
            type: 'hf',
            hf_id: 'accuracy',
            git_commit_sha: '8b9373dc8693ffe0244a52551ac5573cffa503aa',
            best_score: 1.0,
        },
        {
            type: 'hf',
            hf_id: 'f1',
            git_commit_sha: '8b9373dc8693ffe0244a52551ac5573cffa503aa',
            best_score: 1.0,
        },
    ],

    preparation_strategies: {
        prompt_based_testing: {
            prompt_builder: {
                instruction_zero_shot: '',
                instruction_few_shot: '',
                input_prefix: '',
                output_prefix: '',
                append_choices_to_input: false,
                choices_prefix: '',
                choice_item_postfix: '',
                choice_item_prefix: '',
                permute_choices: false,
                few_shot_example_separator: '\n\n',
                stop_string: '.',
            },
        },
    },
}