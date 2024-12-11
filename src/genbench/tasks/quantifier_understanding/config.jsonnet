{
    name: 'Quantifier Understanding',
    description: 'The task evaluates generalization in the understanding of quantifiers. It aims to measure
                  how well can language models capture the semantics of logical quantifiers in language.
                  ',
    keywords: [
        'quantifiers',
        'LLM',
        'prompting',
        'semantics'
    ],

    authors: [
        'Leroy Wang',
        'Shane Steinert-Threlkeld'
    ],

    data_source: {
        type: 'manual',
        test: 'https://raw.githubusercontent.com/lerow/genbench_cbt/quantifier_understanding/src/genbench/tasks/quantifier_understanding/test_data.jsonl',
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
        prompt_based_testing: {
            prompt_builder: {
                instruction_zero_shot: '',  // Left empty because the prompt is in the data
                instruction_few_shot: '',   // Left empty because the prompt is in the data
                input_prefix: 'Q: ',
                output_prefix: '\nA: ',
            }
        },
    },
}
