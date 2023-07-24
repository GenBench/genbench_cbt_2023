{
    name: 'Shifted Pauq (ru_pauq_target_length_split)',

    description: 'Shifted Pauq (en_pauq_target_length_split) aims to measure compositional generalization of on text2sql dataset with splits based on target length. Input language is Russian. Short queries are in test, while long queries are in train. Split was made on 30 percentile of dataset token length. To measure compostional distribution, it was made certain, that all of test tokens of target queries are present in train set.',

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
        hf_id: ['composite/pauq', 'ru_pauq_tl'],
        git_commit_sha: 'ddb9c0830ad37b084304e712eaacf02145c656e5',
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