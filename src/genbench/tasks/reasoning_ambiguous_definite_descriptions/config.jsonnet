{
    name: 'reasoning_ambiguous_definite_descriptions',

    description: 'Reasoning about Ambiguous Definite Descriptions aims to evaluate how well Large Language Models can use explicit reasoning to resolve ambiguity in language',

    keywords: [
        'natural language reasoning',
        'definite descriptions',
        'ambiguity',
        'large language models',
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
        target: 'target',
        target_options: 'target_options'
    },

    evaluation_metrics: [
        {
            hf_id: 'accuracy',
            git_commit_sha: '34d6add55811828baef83e0d7c6826e2193f7b6a',
            best_score: 1.0,
        },
        {
            hf_id: 'f1',
            git_commit_sha: '3a4c40f7397dcd7d9dccf0659616dc6b14072dcb',
            best_score: 1.0,
        },
    ],

    preparation_strategies: {
        prompt_based_testing: {
            prompt_builder: {
                instruction_zero_shot: '',
                instruction_few_shot: '',
                input_prefix: '',
                output_prefix: '\n\nOption ',
                append_choices_to_input: false,
                choices_prefix: '',
                choice_item_postfix: '',
                choice_item_prefix: '',
                permute_choices: false,
                few_shot_example_separator: '\n\n\n',
                stop_string: '.',
            },
        },
    },
}