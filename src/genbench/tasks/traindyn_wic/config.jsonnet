{
    name: 'Dummy training dynamics resplitting',
    description: 'In this split, we take the GLUE dataset WiC, and resplit it according to the training accuracies the data points obtain when training the model on all datapoints.',

    keywords: [
        'non-i.i.d. generalisation',
        'training dynamics',
        'dataset cartography'
    ],

    authors: [
        'Verna Dankers',
    ],

    data_source: {
        type: 'hf',
        hf_id: ['super_glue', 'wic'],
        git_commit_sha: 'd05df0885fb0a37b9a05ae5a6cf7084fc2b309c4',
    },

    has_validation_set: true,
    has_train_set: true,
    task_type: 'multiple_choice',
    field_mapping: {
        input: 'word',
        input2: 'sentence1',
        input3: 'sentence2',
        target: 'label',
    },

    split_file: 'split.jsonnet',
    evaluation_metrics: [
        {
            hf_id: 'accuracy',
            git_commit_sha: '34d6add55811828baef83e0d7c6826e2193f7b6a',
            best_score: 1.0
        },
    ],

    preparation_strategies: {
        finetuning: {
            objective: 'maximum_likelihood',
        },

    },
}
