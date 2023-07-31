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
        test: 'https://raw.githubusercontent.com/MaikeZuefle/genbench_cbt/latent_feature_split/src/genbench/tasks/hate_speech_detection/reddit_test.jsonl'
        // validation: 'https://raw.githubusercontent.com/MaikeZuefle/genbench_cbt/latent_feature_split/src/genbench/tasks/hate_speech_detection/reddit_test.jsonl',
        //train: 'https://raw.githubusercontent.com/MaikeZuefle/genbench_cbt/latent_feature_split/src/genbench/tasks/hate_speech_detection/reddit_test.jsonl'
    },

    has_validation_set: false,
    has_train_set: false,

    task_type: 'multiple_choice',

    evaluation_metrics: [
        {
            hf_id: 'accuracy',
            best_score: 1.0,
            git_commit_sha: '34d6add55811828baef83e0d7c6826e2193f7b6a',
        },
        {
            hf_id: 'f1', 
            best_score: 1.0,
            git_commit_sha: '3a4c40f7397dcd7d9dccf0659616dc6b14072dcb',
        },
        {
            hf_id: 'roc_auc', 
            best_score: 1.0,
            git_commit_sha: 'fb95becece31595a0c04cd1ae9e50ab8e60e9564'
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