{
    name: 'Europarl DBCA splits (comdiv0_el)',

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
    
    task_type: 'free_form',
    
    data_source: {
        type: 'hf',
        hf_id: ['Anssi/europarl_dbca_splits', 'comdiv0.0_en_el'],
        git_commit_sha: '0dcb7abe8e18aa520cbfcbe9141b916c684912fc'
    },

    evaluation_metrics: [
        {
            hf_id: 'chrf',
            git_commit_sha: '4b119256e85de9130aa84d87247381c5acb29bc1',
            best_score: 100.0,
        }
    ],

    has_validation_set: false,
    has_train_set: true,

    preparation_strategies: {
        finetuning: {
            objective: 'maximum_likelihood',
        },
    },
}