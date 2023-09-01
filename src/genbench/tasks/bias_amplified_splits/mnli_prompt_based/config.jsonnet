{
    name: 'Bias-amplified Splits (MultiNLI - Prompt-based)',

    description: 'We take MultiNLI (MNLI) and extract a bias-amplified training set and an anti-biased test set for it from the original splits. For resplitting, we use a novel clustering-based approach to detect anti-biased minority examples.',

    keywords: [
        'non-i.i.d. generalization',
        'dataset biases',
        'minority examples',
        'robustness',
        'prompting',
        'LLMs'
    ],

    authors: [
        'Yuval Reif',
        'Roy Schwartz'
    ],

    data_source: {
        type: 'hf',
        hf_id: ['glue', 'mnli'],
        git_commit_sha: 'fd8e86499fa5c264fcaad392a8f49ddf58bf4037'
    },

    has_validation_set: true,
    has_train_set: true,

    task_type: 'free_form',

    field_mapping: {
        input: 'input',
        target: 'target'
    },

    split_file: 'split.jsonnet',

    evaluation_metrics: [
        {
            hf_id: 'exact_match',
            git_commit_sha: "758135da6a37ce962b7bc38c6dd5eab672d2b742",
            best_score: 1.0
        }
    ],
    preparation_strategies: {
        prompt_based_testing: {
            prompt_builder: {
                instruction_zero_shot: 'In this task, you are given a pair of sentences, sentence 1 and sentence 2. Your job is to determine if the two sentences clearly agree/disagree with each other, or if this cannot be determined. Indicate your answer as yes, no or maybe respectively.\n\n',
                instruction_few_shot: 'In this task, you are given a pair of sentences, sentence 1 and sentence 2. Your job is to determine if the two sentences clearly agree/disagree with each other, or if this cannot be determined. Indicate your answer as yes, no or maybe respectively.\nHere are some examples:\n\n',
                append_choices_to_input: false,
                few_shot_example_separator: '\n',
                stop_string: '\n\n'
            }
        }
    }
}