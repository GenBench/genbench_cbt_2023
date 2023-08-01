{
    name: 'Multilingual SCAN',

    // @TODO: Add a description of the task
    description: 'Multilingual SCAN aims to measure ...',

    // @TODO: Add a list of keywords that describe the task
    keywords: [
        'multilingual',
        'compositional',
    ],

    authors: [
        'Amélie Reymond',
        ' Shane Steinert-Threlkeld',
    ],

    data_source: {
        type: 'manual',
        test: 'https://somewebsite.com/path/to/test.jsonl',
    },

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