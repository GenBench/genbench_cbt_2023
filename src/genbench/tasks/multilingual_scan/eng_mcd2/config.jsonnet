{
    name: 'mSCAN (language: eng, split: mcd2)',

    // @TODO: Add a description of the task
    description: 'Multilingual SCAN (eng) aims to measure ...',

    // @TODO: Add a list of keywords that describe the task
    keywords: [
        'keyword1',
        'keyword2',
    ],

    authors: [
        'Amélie Reymond',
        'Shane Steinert-Threlkeld',
    ],

    data_source: {
        type: 'manual',
        train: 'https://huggingface.co/datasets/ameliettr/mSCAN/raw/main/eng/mcd2/train.jsonl',
        test: 'https://huggingface.co/datasets/ameliettr/mSCAN/raw/main/eng/mcd2/test.jsonl',
        validation: 'https://huggingface.co/datasets/ameliettr/mSCAN/raw/main/eng/mcd2/dev.jsonl',
    },

    has_validation_set: true,
    has_train_set: true,

    task_type: 'free_form',

    preparation_strategies: {
        finetuning: {
            objective: 'maximum_likelihood',
        },

        prompt_based_testing: {
            prompt_builder: {
                instruction_zero_shot: '',
                input_prefix: 'IN: ',
                output_prefix: 'OUT: ',
                append_choices_to_input: false,
                few_shot_example_separator: '\n\n',
                stop_string: '\n\n',
            }
        },

    },

    evaluation_metrics: [
        {
            hf_id: 'exact_match',
            git_commit_sha: "758135da6a37ce962b7bc38c6dd5eab672d2b742",
            best_score: 1.0,
        }
    ]
}