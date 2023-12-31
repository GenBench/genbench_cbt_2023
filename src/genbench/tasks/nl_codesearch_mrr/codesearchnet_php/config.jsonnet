{
    name: 'Natural Language Codesearch Ranking (codesearchnet_php)',

    description: 'Natural Language Codesearch Ranking (codesearchnet_php) aims to measure the generalization capabilites of language models in code understanding. This subtasks measures cross-lingual generalization',

    keywords: [
        'codesearch',
        'natural language query',
        'mean reciprocal rank',
        'php',
        'cross-lingual',
    ],

    authors: [
        'Andor Diera',
        'Abdelhalim Dahou',
		'Lukas Galke',
		'Fabian Karl',
        'Florian Sihler',
		'Ansgar Scherp',  
    ],

    data_source: {
        type: 'manual',
        test: 'https://zenodo.org/record/8310891/files/test_php.jsonl',
        train:'https://zenodo.org/record/8310891/files/train_adv.jsonl',
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