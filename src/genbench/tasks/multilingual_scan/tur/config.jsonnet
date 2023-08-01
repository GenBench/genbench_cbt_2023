{
    name: 'Multilingual SCAN (tur)',

    // @TODO: Add a description of the task
    description: 'Multilingual SCAN (tur) aims to measure ...',

    // @TODO: Add a list of keywords that describe the task
    keywords: [
        'keyword1',
        'keyword2',
    ],

    authors: [
        'Amélie Reymond',
        ' Shane Steinert-Threlkeld',
        
    ],

    data_source: {
        type: 'manual',
        test: 'https://raw.githubusercontent.com/GenBench/genbench_cbt/main/src/genbench/dummy_data/LLM_test.jsonl',
    },

    has_validation_set: false,
    has_train_set: false,

    task_type: 'free_form',

    evaluation_metrics: [
        {
            hf_id: 'exact_match',
            git_commit_sha: "758135da6a37ce962b7bc38c6dd5eab672d2b742",
            best_score: 1.0,
        }
    ]
}