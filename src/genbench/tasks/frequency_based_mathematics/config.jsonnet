{
    name: 'Frequency based mathematics',
    description: 'This sample submission measures generalisation in the domain of mathematical
                  questions, by quantifying the extent to which correctness depends on the 
                  frequency of the underlying terms. A model is said to be a stronger at
                  generalisation if its answers are less dependent on the term frequencies.
                  This test is inspired by the work of Razeghi et al (2022).
                  and the performance.
                  ',
    keywords: [
        'mathematics',
        'term_frequencies',
        'prompting',
        'LLMs'
    ],

    authors: [
        'Dieuwke Hupkes',
    ],

    data_source: {
        type: 'manual',
        test: 'https://raw.githubusercontent.com/dieuwkehupkes/genbench_cbt_sample_submission/frequency_math/src/genbench/tasks/frequency_based_mathematics/test_data.jsonl',
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
