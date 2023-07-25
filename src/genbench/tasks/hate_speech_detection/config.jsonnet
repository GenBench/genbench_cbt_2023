{
    name: 'Hate Speech Detection',

    // @TODO: Add a description of the task
    description: 'Hate speech detection is the task of detecting offensive or hateful language in communication. Usually,
    such speech is directed towards a person or a group of people based on some characteristics like religion, gender
    ethnicity etc.',

    // @TODO: Add a list of keywords that describe the task
    keywords: [
        'hate speech',
        'social media',
    ],

    authors: [
        'Maike Züfle',
        'Verna Dankers',
        'Ivan Titov',
        
    ],

    data_source: {
        type: 'manual',
        test: 'https://github.com/hate-alert/HateXplain/blob/master/Data/dataset.json',
        train: ''
    },

    has_validation_set: false,
    has_train_set: false,

    task_type: 'multi-choice',

    evaluation_metrics: [
        {
            hf_id: 'accuracy',
        },
        {
            hf_id: 'f1', 
        },
        {
            hf_id: 'roc_auc', 
        },
    ],

    preparation_strategies: {
        // A recipe for preparing the model to perform the task by configuring its prompt.
        // This recipe is suitable for generative LMs such as GPT-3, OPT, T5, etc.
        // We provide a few options for configuring the prompt. But, the task creator can
        // also provide a custom prompt preparation in the task's Python class.
        finetuning: {
            objective: 'maximum_likelihood',
        }
    },
}