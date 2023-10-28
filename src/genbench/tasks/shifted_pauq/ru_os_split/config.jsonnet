{
    name: 'Shifted Pauq (ru_os_split)',

    description: 'Shifted Pauq in Russian (ru_os_split) aims to measure model ability to generate SQL queries from Russian input with splits generated in i.i.d. strategy.',

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
        hf_id: ['composite/pauq', 'ru_os'],
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