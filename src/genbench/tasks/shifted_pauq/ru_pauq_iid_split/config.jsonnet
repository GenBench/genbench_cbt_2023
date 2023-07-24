{
    name: 'Shifted Pauq (ru_pauq_iid_split)',

    description: 'Shifted Pauq (en_pauq_iid_split) aims to measure model ability to generate SQL queries from Russian input with splits generated in i.i.d. strategy.',

    keywords: [
        'text2sql',
        'iid distribution',
        'multilingual'
    ],

    authors: [
        'Somov Oleg',
        'Dmietrieva Ekaterina',
        'Tutubalina Elena',
    ],

    data_source: {
        type: 'hf',
        hf_id: ['composite/pauq', 'ru_pauq_iid'],
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