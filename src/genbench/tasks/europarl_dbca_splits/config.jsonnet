{
    name: 'Divergent DepRel Distributions',

    description: 'This task aims to measure how well an NMT model generalises to a shifted distribution of
    dependency relations. In practice, this means that the test set includes novel
    (<head lemma>, <deprel>, <dependant lemma>) tuples (=compounds) that were not seen in
    the training set, while having similar relative frequencies of the lemmas and dependency
    relation tags (= elements of the compound tuples = atoms).',

    keywords: [
        'translation',
    ],

    authors: [
        'Anssi Moisio',
    ],

    subtasks_order: [
        'comdiv0_de',
        'comdiv1_de',
        'comdiv0_fr',
        'comdiv1_fr',
        'comdiv0_el',
        'comdiv1_el',
        'comdiv0_fi',
        'comdiv1_fi',
    ],
}
