{
    name: 'Sample LLM  json task',
    description: 'Sample LLM task with dummy data that works with only json, for illustration purposes',

    keywords: [
        'sample_task',
    ],

    authors: [
        'GenBench team',
    ],

    data_source: {
        type: 'manual',
        test: 'https://raw.githubusercontent.com/GenBench/genbench_cbt/main/src/genbench/dummy_data/LLM_test.jsonl', // NB we should host this elsewhere to avoid confusion
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
                instruction_zero_shot: 'Add two numbers together\n\n',
                instruction_few_shot: 'Add two numbers together. Here are some examples: \n\n',
                input_prefix: 'Q: ',
                output_prefix: '\nA: ',
            }
        },
    },
}