{
    name: 'Multilingual SCAN',

    description: 'Multilingual SCAN aims to measure compositional and cross-lingual generalization in multilingual LLMs.',

    keywords: [
        'cross-lingual',
        'compositional',
        'LLMs',
    ],

    authors: [
        'Amélie Reymond',
        'Shane Steinert-Threlkeld',
    ],

    data_source: {
        type: 'manual',
        test: 'https://somewebsite.com/path/to/test.jsonl',
    },

    # TODO: provide finetuning set
    has_train_set: true,


    task_type: 'free_form',

    preparation_strategies: {
        finetuning: {
            objective: 'maximum_likelihood',
        },
    }

    subtasks_order: [
        'fra',
        'rus',
        'cmn',
        'tur',
        'hin',
        
    ],
}