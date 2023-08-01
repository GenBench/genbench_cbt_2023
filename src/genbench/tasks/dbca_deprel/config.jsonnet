{
    name: 'Divergent DepRel Distributions',

    description: 'This task aims to measure how well an NMT model generalises to a shifted distribution of
    dependency relations. In practice, this means that the test set includes novel
    (<head lemma>, <deprel>, <dependant lemma>) tuples (=compounds) that were not seen in
    the training set, while having similar relative frequencies of the lemmas and dependency
    relation tags (= elements of the compound tuples = atoms).',

    keywords: [
        'translation',
        'dependency relations',
    ],

    authors: [
        'Anssi Moisio',
    ],

    // HF dataset fails because loading the data requires extra kwargs "lang1" and "lang2":
    // load_dataset("europarl_bilingual", lang1="en", lang2="fi")
    // data_source: {
    //     type: 'hf',
    //     hf_id: ['europarl_bilingual', 'en-fi'],
    //     git_commit_sha: 'd53ac07927a7d3bece24ea465bbeac4cbe51d681'
    // },

    data_source: {
        type: 'manual',
        train: 'https://raw.githubusercontent.com/anmoisio/genbench_cbt/be64488a106dcf8bc5bd7d58f9eb972718e9e6b8/src/genbench/tasks/dbca_deprel/train.jsonl',
        test: 'https://raw.githubusercontent.com/anmoisio/genbench_cbt/be64488a106dcf8bc5bd7d58f9eb972718e9e6b8/src/genbench/tasks/dbca_deprel/test.jsonl',
    },

    has_validation_set: false,
    has_train_set: true,

    task_type: 'free_form',

    evaluation_metrics: [
        // BLEU and chrF fail tests because their output includes other info besides the score
        // e.g. bleu fails tests/test_task.py:186: "assert [1.0, 1.0, 1.0, 1.0] == 1.0"
        // {
        //     hf_id: ['bleu', 'bleu'],
        //     git_commit_sha: 'b873385fa78c05529c1dbe09fb0357a4b510af76',
        //     best_score: 1.0,
        // }
        // {
        //      hf_id: 'chrf',
        //      git_commit_sha: '4b119256e85de9130aa84d87247381c5acb29bc1',
        //      best_score: 100.0,
        // }
    ],

    preparation_strategies: {
        finetuning: {
            // cross-entropy?
            objective: 'maximum_likelihood',
        },
    },
}
