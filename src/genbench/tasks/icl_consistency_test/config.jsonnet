{
    name: 'ICL consistency test',

    // @TODO: Add a description of the task
    description: 'ICL consistency test aims to measure the consistency of LLM predictions across many different settings on the same datapoint',

    // @TODO: Add a list of keywords that describe the task
    keywords: [
        'consistency',
        'LLM',
        'robustness',
        'in-context learning',
        'icl',
        
    ],

    authors: [
        'Lucas Weber',
        'Elia Bruni',
        'Dieuwke Hupkes',
        
    ],

    data_source: {
        type: 'manual',
        // 'https://raw.githubusercontent.com/LucWeber/icl_consistency_data/main/data/genbench_all.jsonl',
        test: 'https://drive.google.com/file/d/12K-qg66PTmlvzmpID_kijMjbixFT_juN/view?usp=sharing', 
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
                instruction_zero_shot: '',
                instruction_few_shot: '',
                input_prefix: '',
                output_prefix: '',
            }
        },
    },
}
