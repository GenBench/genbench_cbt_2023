{
    name: 'Natural Language Codesearch Classification (webquery)',

    // @TODO: Add a description of the task
    description: 'Natural Language Codesearch Classification (webquery) aims to measure the generalization capabilites of language models in code understanding. This subtasks measures robustness in covariate shift',

    // @TODO: Add a list of keywords that describe the task
    keywords: [
        'codesearch',
        'natural language query',
		'binary classification',
		'python',
		'robustness',
		'covariate shift'
    ],

    authors: [
        'Andor Diera',
        'Abdelhalim Dahou',
        'Florian Sihler',
        
    ],

    data_source: {
        type: 'manual',
        test: 'https://raw.githubusercontent.com/GenBench/genbench_cbt/main/src/genbench/dummy_data/LLM_test.jsonl',
    },

    has_train_set: true,

    task_type: 'multi_choice',

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
        prompt_based_testing: {
            prompt_builder: {
                instruction_zero_shot: 'Add two numbers together\n\n',
                instruction_few_shot: 'Add two numbers together. Here are some examples: \n\n',
                input_prefix: 'Q: ',
                output_prefix: '\nA: ',
            }
        },
    },
}