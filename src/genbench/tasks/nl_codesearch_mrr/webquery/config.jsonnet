{
    name: 'Natural Language Codesearch Ranking (webquery)',

    description: 'Natural Language Codesearch Ranking (webquery) aims to measure the generalization capabilites of language models in code understanding. This subtasks measures robustness in covariate shift',

    keywords: [
        'codesearch',
        'natural language query',
        'mean reciprocal rank',
        'python',
        'robustness',
        'covariate shift',
    ],

    authors: [
        'Andor Diera',
        'Abdelhalim Dahou',
        'Florian Sihler',
        
    ],

    data_source: {
        type: 'manual',
        test: 'https://raw.githubusercontent.com/drndr/genbench_ds/master/sample_data/mrr/webquery/test_sample_cbt.jsonl',
        train:'https://raw.githubusercontent.com/drndr/genbench_ds/master/sample_data/mrr/codesearchnet_adv/train_sample_cbt.jsonl',
    },

    has_validation_set: false,
    has_train_set: true,

    task_type: 'multiple_choice',

    evaluation_metrics: [
        {
        hf_id: 'accuracy',
        git_commit_sha: '34d6add55811828baef83e0d7c6826e2193f7b6a',
        best_score: 1.0,
	    },
    ],

    preparation_strategies: {
        finetuning: {
            objective: 'maximum_likelihood',
        },
    },
}