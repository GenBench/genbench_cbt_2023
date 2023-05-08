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
        test: 'https://github.com/GenBench/genbench_cbt/dummy_data/LLM_test.jsonl', // NB we should host this elsewhere to avoid confusion
    },

    has_validation_set: false,
    has_train_set: false,

    task_type: 'free_form',

    evaluation_metrics: [
        {
            type: 'hf',
            path: ['EM'],
        }
    ],

    model_prepation_strategies: {
        // A recipe for preparing the model to perform the task by configuring its prompt.
        // This recipe is suitable for generative LMs such as GPT-3, OPT, T5, etc.
        // We provide a few options for configuring the prompt. But, the task creator can
        // also provide a custom prompt preparation in the task's Python class.
        in_context_learning: {
            instruction: 'Add two numbers together',
            input_prefix: 'Q: ',
            output_prefix: 'A: ',
        },
    },
}