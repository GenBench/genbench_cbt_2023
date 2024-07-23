{
    name: 'Shifted Pauq (en_tsl_split)',

    description: 'Shifted Pauq (en_tsl_split) aims to measure compositional generalization of on text2sql dataset with splits based on target length. Input language is English. Long query templates are in test, while short query templates are in train. To measure compostional distribution, it was made certain, that all of test tokens of target queries are present in train set.',

    keywords: [
        'text2sql',
        'label shift',
        'compositional generalization',
    ],

    authors: [
        'Somov Oleg',
        'Dmietrieva Ekaterina',
        'Tutubalina Elena',
    ],

    data_source: {
        type: 'hf',
        hf_id: ['composite/pauq', 'en_tsl'],
        git_commit_sha: '63e3e9329f785d097f4746618737d69530d1cdb4',
    },

    has_validation_set: false,
    has_train_set: true,

    task_type: 'free_form',

    field_mapping: {
        input: 'question',
        target: 'query'
    },

    evaluation_metrics: [
        {
            hf_id: 'evaluate-metric/exact_match',
            best_score: 1.0,
            git_commit_sha: '8e612716f2b1b08d23b0b2d7aa667d2f38eb989e'
        }
    ],

    preparation_strategies: {
        finetuning: {
            objective: 'maximum_likelihood',
        }
    }
}