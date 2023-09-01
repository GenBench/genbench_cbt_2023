{
    name: 'Bias-amplified Splits',

    description: 'In Bias-amplified Splits, we argue that to promote models robust to subtle biases, we should in fact *amplify* dataset biases during evaluation, instead of attempting to balance and remove them. We take existing datasets and extract a bias-amplified training set and an anti-biased test set from the original splits. For resplitting, we use a novel clustering-based approach to detect anti-biased minority examples.',

    keywords: [
        'non-i.i.d. generalization',
        'dataset biases',
        'minority examples',
        'robustness'
    ],

    authors: [
        'Yuval Reif',
        'Roy Schwartz'
    ],

    subtasks_order: [
        'mnli',
        'mnli_prompt_based',
        'wanli',
        'wanli_prompt_based',
        'qqp',
    ],
}