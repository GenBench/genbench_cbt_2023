{
    name: 'Multilingual SCAN (hin)',

    description: 'Multilingual SCAN (hin) aims to measure compositional and cross-lingual generalization in multilingual LLMs',

    keywords: [
        'cross-lingual',
        'compositional',
        'hindi',
    ],

    authors: [
        'Amélie Reymond',
        'Shane Steinert-Threlkeld',
        
    ],

    data_source: {
        type: 'manual',
        test: 'https://raw.githubusercontent.com/amelietamreymond/genbench_cbt/multilingual_scan/src/genbench/tasks/multilingual_scan/hin/sample.jsonl',
    },

    has_validation_set: false,
    has_train_set: false,

    task_type: 'free_form',

    preparation_strategies: {
        finetuning: {
            objective: 'maximum_likelihood',
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