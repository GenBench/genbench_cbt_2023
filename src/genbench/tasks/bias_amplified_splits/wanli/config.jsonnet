{
    name: 'Bias-amplified Splits (WANLI)',

    description: 'We take WANLI and extract a bias-amplified training set and an anti-biased test set for it from the original splits. For resplitting, we use a novel clustering-based approach to detect anti-biased minority examples.',

    keywords: [
        'non-i.i.d. generalization',
        'dataset biases',
        'minority examples',
        'robustness'
    ],

    authors: [
        'Yuval Reif',
        'Roy Schwartz'
    ],

    data_source: {
        type: 'hf',
        hf_id: 'alisawuffles/WANLI',
        git_commit_sha: '61c95318fd71c55b6ba355d76253254615f387ec',
    },

    has_validation_set: true,
    has_train_set: true,

    task_type: 'multiple_choice',

    field_mapping: {
        input: 'sentence_pair',
        target: 'label',
    },

    split_file: 'split.jsonnet',

    evaluation_metrics: [
        {
            hf_id: 'accuracy',
            git_commit_sha: '34d6add55811828baef83e0d7c6826e2193f7b6a',
            best_score: 1.0,
        }
    ],

    preparation_strategies: {
        // Finetuning the model on the task's train-set and then evaluating
        // on the task's test-set. This is suitable for models such as RoBERTa, BERT, etc.,
        // but can be used for LLMs as well.
        finetuning: {
            objective: 'maximum_likelihood',
            // ... other model-agnostic finetuing options ...
        }
    },
}