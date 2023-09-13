{
    name: 'OperationsResearchQA (cot)',

    description: 'ORQA (or Operations Research QA) is a benchmark to study the generalizability of PLMs towards operations research. We want to ask the question, "Can PLMs reason about operations research?"',

    keywords: [
        'Operations Research',
        'Question Answering',
        'Domain Specialization',
        'Practical',
        'Cross Domain',
        'Covariate Shift',
        'Naturally Occuring Shift Source',
        'Pretrain-test Shift Locus',
        'Knowledge Multiple Choice QA',
        'Optimization Modeling',
        'Reasoning',
        'Context',
        'Large Language Models',
    ],

    authors: [
        'Rindra Ramamonjison',
        'Mahdi Mostajabdaveh',
        'Timothy Yu',
        'Giuseppe Carenini',
        'Samarendra Dash',
        'Serge Jabo Byusa',
        'Zirui Zhou',
        'Yong Zhang',
    ],

    data_source: {
        type: 'manual',
        test: 'https://raw.githubusercontent.com/OpResearchQA/ORQA_data/main/test_dataset.jsonl', // link to our sample test set
        validation: 'https://raw.githubusercontent.com/OpResearchQA/ORQA_data/main/val_dataset.jsonl', // link to our sample dev set
    },

    has_validation_set: true,
    has_train_set: false,

    task_type: 'multiple_choice',


    evaluation_metrics: [
        {
            hf_id: 'accuracy',
            git_commit_sha: '34d6add55811828baef83e0d7c6826e2193f7b6a',
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
                instruction_zero_shot: '["Given the context (following Context:), provide the chain of thoughts (following Reasoning:) to solve the question (following Question:). Remember, only one option is correct.\\n", "Given the context (following Context:), the reasoning (following Reasoning:), select the most appropriate answer to the question (following Question:). Answer only \'A\', \'B\', \'C\', or \'D\'. There is only one correct answer.\\n"]',
                instruction_few_shot: '["Given the context (following Context:), provide the chain of thoughts (following Reasoning:) solve to the question (following Question:). Remember, only one option is correct.\\n\\nHere are some examples: \\n\\n", "Given the context (following Context:), the reasoning (following Reasoning:), select the most appropriate answer to the question (following Question:). Answer only \'A\', \'B\', \'C\', or \'D\'. There is only one correct answer.\\n\\nHere are some examples: \\n\\n"]',
                output_prefix: '["\\nReasoning: Let\'s think step by step ", "\\nAnswer: Among A through D, the answer is ("]',
                input_prefix: '', // no input prefix since Question follows Context
                append_choices_to_input: false,
                few_shot_example_separator: '["\\n\\n", ")\\n\\n"]',
            }
        },
    },
}