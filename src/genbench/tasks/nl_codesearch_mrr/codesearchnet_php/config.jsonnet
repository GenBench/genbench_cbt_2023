{
    name: 'Natural Language Codesearch Ranking (codesearchnet_php)',

    // @TODO: Add a description of the task
    description: 'Natural Language Codesearch Ranking (codesearchnet_php) aims to measure the generalization capabilites of language models in code understanding. This subtasks measures cross-lingual generalization',

    // @TODO: Add a list of keywords that describe the task
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
        'Florian Sihler',
        
    ],

    data_source: {
        type: 'manual',
        test: 'https://raw.githubusercontent.com/drndr/genbench_ds/master/sample_data/mrr/codesearchnet_php/test_sample_cbt.jsonl',
		train:'https://raw.githubusercontent.com/drndr/genbench_ds/master/sample_data/clf/codesearchnet_adv/train_sample_cbt.jsonl',
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
        // A recipe for preparing the model to perform the task by configuring its prompt.
        // This recipe is suitable for generative LMs such as GPT-3, OPT, T5, etc.
        // We provide a few options for configuring the prompt. But, the task creator can
        // also provide a custom prompt preparation in the task's Python class.
		finetuning: {
            objective: 'maximum_likelihood',
        },
    },
}