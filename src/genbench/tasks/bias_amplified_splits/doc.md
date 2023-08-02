## Motivation
NLP models often rely on superficial cues known as *dataset biases* to achieve impressive performance, and can fail on examples where these biases do not hold. 
Recent work sought to develop robust, unbiased models by filtering *biased* examples from training sets. We argue that such filtering can obscure the true capabilities of models to overcome biases, which might never be removed in full from the dataset. 

We propose that in order to drive the development of models robust to subtle biases, dataset biases should in fact be **amplified** in the training set. 
We introduce **bias-amplifed splits**, an evaluation framework defined by a *bias-amplified* training set and an *anti-biased* test set, both automatically extracted from existing datasets. 
To extract *biased* and *anti-biased* examples, we use a novel clustering-based approach for detecting minority examples in the dataset.

## Examples
Bias-amplified splits can be created for various tasks. Each of the sub-tasks is for a different dataset -- see examples in each sub-task's documentation.

## Data Source
We extract bias-amplified splits from existing datasets. All datasets can be obtained via the Hugging Face dataset hub. See references and license details in each of the subtasks.

## Limitations and Bias
TODO: *Note any known limitations or biases that the Bias-amplified Splits has, with links and references if possible.*

## Citation
```
@inproceedings{reif-schwartz-2023-fighting,
    title = "Fighting Bias With Bias: Promoting Model Robustness by Amplifying Dataset Biases",
    author = "Reif, Yuval  and
      Schwartz, Roy",
    booktitle = "Findings of the Association for Computational Linguistics: ACL 2023",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.findings-acl.833",
    pages = "13169--13189",
    abstract = "NLP models often rely on superficial cues known as dataset biases to achieve impressive performance, and can fail on examples where these biases do not hold. Recent work sought to develop robust, unbiased models by filtering biased examples from training sets. In this work, we argue that such filtering can obscure the true capabilities of models to overcome biases, which might never be removed in full from the dataset. We suggest that in order to drive the development of models robust to subtle biases, dataset biases should be amplified in the training set. We introduce an evaluation framework defined by a bias-amplified training set and an anti-biased test set, both automatically extracted from existing datasets. Experiments across three notions of bias, four datasets and two models show that our framework is substantially more challenging for models than the original data splits, and even more challenging than hand-crafted challenge sets. Our evaluation framework can use any existing dataset, even those considered obsolete, to test model robustness. We hope our work will guide the development of robust models that do not rely on superficial biases and correlations. To this end, we publicly release our code and data.",
}
```

## Further References
TODO: *Add any useful further references.*

