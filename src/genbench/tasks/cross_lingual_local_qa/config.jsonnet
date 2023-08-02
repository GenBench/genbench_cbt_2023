{
    name: 'Cross-lingual Local QA',

    // Add a description of the task
    description: 'Cross-lingual Local QA aims to measure the presence of local and culture-specific knowledge in LLMs, as well as its generalisation across languages.',

    // Add a list of keywords that describe the task
    keywords: [
        'cross-lingual',
        'multilingual'
        'knowledge generalisation',
        'LLM evaluation',
        'QA',
    ],

    authors: [
        'Lea Krause',
        ' Wondimagegnhue Tsegaye Tufa',
        ' Selene Báez Santamaría',
        ' Urja Khurana',
        ' Angel Daza',
        ' Piek Vossen',
        
    ],

    data_source: {
        type: 'manual',
        test: 'https://raw.githubusercontent.com/GenBench/genbench_cbt/main/src/genbench/dummy_data/CLL-QA_test.jsonl',
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
    ],

    preparation_strategies: {
        // A recipe for preparing the model to perform the task by configuring its prompt.
        // This recipe is suitable for generative LMs such as GPT-3, OPT, T5, etc.
        // We provide a few options for configuring the prompt. But, the task creator can
        // also provide a custom prompt preparation in the task's Python class.
    },
}
