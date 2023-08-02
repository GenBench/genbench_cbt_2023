{
    name: 'OOV Generalisation (dow)',

    // @TODO: Add a description of the task
    description: 'OOV Generalisation (dow) aims to measure ...',

    // @TODO: Add a list of keywords that describe the task
    keywords: [
        'subword tokenization',
        'OOV',
        'OOV generalisation',
        'OOD generalisation',
        'text classificaiton'
    ],

    authors: [
        'Khuyagbaatar Batsuren',
        'TBD',
        
    ],

    data_source: {
        type: 'manual',
        train: 'https://raw.githubusercontent.com/kbatsuren/genbench_cbt/main/src/genbench/oov_generalisation/dow/train.jsonl',
        validation: 'https://raw.githubusercontent.com/kbatsuren/genbench_cbt/main/src/genbench/oov_generalisation/dow/validation.jsonl',
        test: 'https://raw.githubusercontent.com/kbatsuren/genbench_cbt/main/src/genbench/oov_generalisation/dow/test.jsonl',
    },

    has_validation_set: true,
    has_train_set: true,
    task_type: 'multiple_choice',

    evaluation_metrics: [
        {
            hf_id: 'accuracy',
        }
    ],

    preparation_strategies: {
        // A recipe for preparing the model to perform the task by configuring its prompt.
        // This recipe is suitable for generative LMs such as GPT-3, OPT, T5, etc.
        // We provide a few options for configuring the prompt. But, the task creator can
        // also provide a custom prompt preparation in the task's Python class.
        prompt_based_testing: {
            prompt_builder: {
                instruction_zero_shot: 'Classify if word and definition matches: True or False?\n\n',
                instruction_few_shot: 'Classify if word and definition matches: True or False? Here are some examples: \n\n',
                input1_prefix: 'W: ',
                input2_prefix: 'D: ',
                output_prefix: '\nA: ',
            }
        },
        finetuning: {
            objective: 'maximum_likelihood',
        },
    },
}