{
    name: 'Shifted Pauq',

    description: 'Shifted Pauq aims to measure compositional generalization in task of text2sql on different label shift splits.',

    keywords: [
        'compositional generalization',
        'text2sql',
        'distribution shift',
        'multilingual'
    ],

    authors: [
        'Somov Oleg',
        'Dmietrieva Ekaterina',
        'Tutubalina Elena',
    ],

    subtasks_order: [
        'ru_pauq_target_length_split',
        'en_pauq_target_length_split',
        'ru_pauq_iid_split',
        'en_pauq_iid_split',
    ],
}