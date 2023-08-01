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
        ' Peter Bloem',
        ' Ilia Markov',
        ' Piek Vossen',
        
    ],

    data_source: {
        type: 'manual',
        test: '',
    },

    has_validation_set: false,
    has_train_set: false,

    task_type: 'multiple_choice',

    field_mapping: {
        input: 'input',
        target: 'label_nr',
    }

    evaluation_metrics: [
        {
            hf_id: 'accuracy',
        },
        {
            hf_id: 'f1',
        },
    ],

    preparation_strategies: {
        prompt_based_testing: {
            instruction_few_shot: '',
            input_prefix: '',
            output_prefix: '',
            append_choices_to_input: False,
            choices_prefix: '',
            choice_item_postfix: '',
            choice_item_prefix: '',
            permute_choices: False,
            few_shot_example_separator: '\n\n',
            stop_string: '.',
        },
    },
}