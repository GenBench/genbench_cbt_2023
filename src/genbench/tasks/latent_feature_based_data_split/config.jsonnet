{
    name: 'Latent feature based Data Split',

     // @TODO: Add a description of the task
    description: "We split hate speech data based on the internal representations of a RoBERTa model. 
    The o.o.d. data splits leads to an under-representation of parts of the latent space in the 
    model's training set, making the split more challenging than a random split.",

    // @TODO: Add a list of keywords that describe the task
    keywords: [
        'non-i.i.d. generalisation',
        'o.o.d. generalisation',
        'latent-features',
        'hate speech'
    ],

    authors: [
        'Maike Züfle',
        'Verna Dankers',
        'Ivan Titov',

    ],

    data_source: {
        type: 'manual',
        test: 'https://raw.githubusercontent.com/MaikeZuefle/genbench_cbt/latent_feature_split/src/genbench/tasks/latent_feature_based_data_split/roberta_closest_split/hatexplain_roberta_closest_split_test.jsonl',
        train: 'https://raw.githubusercontent.com/MaikeZuefle/genbench_cbt/latent_feature_split/src/genbench/tasks/latent_feature_based_data_split/roberta_closest_split/hatexplain_roberta_closest_split_train.jsonl'
    },

    has_train_set: true,

    task_type: 'multiple_choice',

    evaluation_metrics: [
        {
            hf_id: 'accuracy',
            best_score: 1.0,
            git_commit_sha: '34d6add55811828baef83e0d7c6826e2193f7b6a',
        },
        {
            hf_id: 'f1',
            average: 'macro',
            best_score: 1.0,
            git_commit_sha: '3a4c40f7397dcd7d9dccf0659616dc6b14072dcb',
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